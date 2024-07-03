import numpy as np
import logging

RATIO_DEGREE_TO_KM = 110
RATIO_DEGREE_TO_M = RATIO_DEGREE_TO_KM * 1000
RELAXATION_COUNTS = 8000
R = 6371  # km


def _cal_init_div(u, v, dx, dy):
    _delta_u_d2x = u[1:-1, 2:] - u[1:-1, :-2]
    _d2x = 2 * dx[1:-1, 1:-1]
    _delta_v_d2y = v[2:, 1:-1] - v[:-2, 1:-1]
    _d2y = 2 * dy[1:-1, 1:-1]

    div = np.zeros(u.shape)
    div[1:-1, 1:-1] = _delta_u_d2x / _d2x + _delta_v_d2y / _d2y

    return div


def _cal_init_vor(u, v, dx, dy):
    _delta_v_d2x = v[1:-1, 2:] - v[1:-1, :-2]
    _d2x = 2 * dx[1:-1, 1:-1]
    _delta_u_d2y = u[2:, 1:-1] - u[:-2, 1:-1]
    _d2y = 2 * dy[1:-1, 1:-1]
    vor = np.zeros(u.shape)
    vor[1:-1, 1:-1] = _delta_v_d2x / _d2x - _delta_u_d2y / _d2y

    return vor


def _cal_dx(lat_2d, lon):
    _lon_resolution = lon[2] - lon[1]
    _a = R * np.cos(np.radians(lat_2d))
    dx = _a * np.radians(_lon_resolution)

    return dx


def _cal_dy(lat, var_shape):
    _lat_resolution = lat[2] - lat[1]
    _dy_value = R * np.radians(_lat_resolution)
    dy = np.full(var_shape, _dy_value)

    return dy


def _update_chi_by_div(chi, div, dx_square, dy_square):
    _delta_chi = np.zeros(chi.shape)

    _delta_chi[1:-1, 1:-1] = np.multiply(
        (
            (chi[2:, 1:-1] - 2 * chi[1:-1, 1:-1] + chi[0:-2, 1:-1])
            / dy_square[1:-1, 1:-1]
            - div[1:-1, 1:-1]
        ),
        dx_square[1:-1, 1:-1],
    ) + (chi[1:-1, 2:] - 2 * chi[1:-1, 1:-1] + chi[1:-1, 0:-2])
    chi = chi + 1 / 4 * _delta_chi

    return chi


def _update_psi_by_vor(psi, vor, dx_square, dy_square):
    _delta_psi = np.zeros(psi.shape)
    _delta_psi[1:-1, 1:-1] = np.multiply(
        (
            (psi[2:, 1:-1] - 2 * psi[1:-1, 1:-1] + psi[0:-2, 1:-1])
            / dy_square[1:-1, 1:-1]
            - vor[1:-1, 1:-1]
        ),
        dx_square[1:-1, 1:-1],
    ) + (psi[1:-1, 2:] - 2 * psi[1:-1, 1:-1] + psi[1:-1, 0:-2])
    psi = psi + 1 / 4 * _delta_psi

    return psi


def _cal_dis_to_tc_center(lon_2d, lat_2d, lon_center, lat_center):
    return np.sqrt((lat_2d - lat_center) ** 2 + (lon_2d - lon_center) ** 2)


def _delete_values_outside_tc(var, dis_to_tc_center, tc_radius_in_km: int = 300):
    _tc_radius_in_degree = tc_radius_in_km / RATIO_DEGREE_TO_KM
    var[dis_to_tc_center >= _tc_radius_in_degree] = 0

    return var


def _cal_divergent_wind(chi, dx, dy):
    u_divergent = np.zeros(chi.shape)
    v_divergent = np.zeros(chi.shape)

    u_divergent[1:-1, 1:-1] = (chi[1:-1, 2:] - chi[1:-1, :-2]) / (2 * dx[1:-1, 1:-1])
    v_divergent[1:-1, 1:-1] = (chi[2:, 1:-1] - chi[:-2, 1:-1]) / (2 * dy[1:-1, 1:-1])

    return u_divergent, v_divergent


def _cal_rotational_wind(psi, dx, dy):
    u_rotational = np.zeros(psi.shape)
    v_rotational = np.zeros(psi.shape)

    u_rotational[1:-1, 1:-1] = -(psi[2:, 1:-1] - psi[:-2, 1:-1]) / (2 * dy[1:-1, 1:-1])
    v_rotational[1:-1, 1:-1] = (psi[1:-1, 2:] - psi[1:-1, :-2]) / (2 * dx[1:-1, 1:-1])

    return u_rotational, v_rotational


def _relaxation(u, v, lon, lat, tc_lon, tc_lat):
    var_shape = u.shape
    _lon_2d, _lat_2d = np.meshgrid(lon, lat)

    dy = _cal_dy(lat, var_shape)
    dx = _cal_dx(_lat_2d, lon)

    _div = _cal_init_div(u, v, dx, dy)
    _vor = _cal_init_vor(u, v, dx, dy)

    _dis_to_tc_center = _cal_dis_to_tc_center(_lon_2d, _lat_2d, tc_lon, tc_lat)
    _div_only_in_tc_region = _delete_values_outside_tc(_div, _dis_to_tc_center)
    _vor_only_in_tc_region = _delete_values_outside_tc(_vor, _dis_to_tc_center)

    _dx_square = dx**2
    _dy_square = dy**2

    chi = np.zeros(var_shape)  # Velocity Potential
    psi = np.zeros(var_shape)  # Stream function
    for _ in range(RELAXATION_COUNTS):
        chi = _update_chi_by_div(chi, _div_only_in_tc_region, _dx_square, _dy_square)
        psi = _update_psi_by_vor(psi, _vor_only_in_tc_region, _dx_square, _dy_square)

    _u_divergent, _v_divergent = _cal_divergent_wind(chi, dx, dy)
    _u_rotational, _v_rotational = _cal_rotational_wind(psi, dx, dy)

    u_wo_tc = u - _u_rotational - _u_divergent
    v_wo_tc = v - _v_rotational - _v_divergent
    return u_wo_tc, v_wo_tc


def remove_vortex(u, v, lon, lat, tc_lon, tc_lat):
    U_noTC, V_noTC = _relaxation(u, v, lon, lat, tc_lon, tc_lat)
    U_noTC, V_noTC = _relaxation(U_noTC, V_noTC, lon, lat, tc_lon, tc_lat)

    r = 5
    lon_indexes = [
        i for i, x in enumerate(lon) if (x >= tc_lon - r) & (x <= tc_lon + r)
    ]
    lat_indexes = [
        i for i, x in enumerate(lat) if (x >= tc_lat - r) & (x <= tc_lat + r)
    ]
    U_noTC_tmp = U_noTC.copy()
    V_noTC_tmp = V_noTC.copy()
    for lon_index in lon_indexes:
        for lat_index in lat_indexes:
            U_noTC[lat_index, lon_index] = np.mean(
                U_noTC_tmp[lat_index - 1 : lat_index + 1, lon_index - 1 : lon_index + 1]
            )
            V_noTC[lat_index, lon_index] = np.mean(
                V_noTC_tmp[lat_index - 1 : lat_index + 1, lon_index - 1 : lon_index + 1]
            )
    U_noTC, V_noTC = _relaxation(U_noTC, V_noTC, lon, lat, tc_lon, tc_lat)
    return U_noTC, V_noTC
