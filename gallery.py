import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from ob_tran import GeneralObliqueProjection
from ob_tran_utils import *



def plot_map(name, crs, figsize=(8, 4)):
    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=crs)
    ax.spines['geo'].set(facecolor='white')
    ax.spines['geo'].set(zorder=0)

    lon_ticks = 15
    lat_ticks = 15
    ax.add_feature(
            cfeature.NaturalEarthFeature(
                category='cultural', scale='10m',
                name='admin_0_countries_lakes'),
            facecolor="#32CD32", edgecolor='black', linewidth=0.1)
    ax.gridlines(
            draw_labels=False, color='gray', linewidth=0.5, alpha=0.5, 
            xlocs=range(-180,180,lon_ticks),
            ylocs=range(-90+lat_ticks,90,lat_ticks))
    ax.gridlines(
            draw_labels=False, color='red', linewidth=0.5, alpha=0.5, 
            xlocs=[0, 180], ylocs=[0])

    if 'o_lat_p' in crs.proj4_params:
        print(f"{name}: +proj=ob_tran "
              f"+o_proj={crs.proj4_params['o_proj']} "
              f"+lon_0={crs.proj4_params['lon_0']:.3f} "
              f"+o_lat_p={crs.proj4_params['o_lat_p']:.3f} "
              f"+o_lon_p={crs.proj4_params['o_lon_p']:.3f}")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.savefig(f"./gallery/{name}.png", dpi=300, transparent=True)
    plt.close()




# --------------------------------------------------------------
# Z 軸回転を行い、中心経度を設定
#   -> 新しい極は lon_0+180 となる
#   central_longitude : 120
# Y 軸回転を行い、元の北極点が位置する緯度を設定
#   pole_latitude : 40
# Z 軸回転を行い、元の北極点が位置する経度を設定
#   pole_longitude : -55
# --------------------------------------------------------------
crs = GeneralObliqueProjection(
        ccrs.Mollweide(),
        central_longitude=120,
        pole_latitude=40, pole_longitude=-55)
plot_map('fig1', crs, (8, 4))



# --------------------------------------------------------------
# Z 軸で-137度回転（東経137度が手前に）
# Y 軸で  37度回転（北緯37度が赤道上の位置に持ってくる）
# X 軸で 135度回転
# Y 軸で -50度回転（回転中心を北緯50度の位置に持ってくる）
# --------------------------------------------------------------
r = Ry(-50) @ Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mollweide(),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig2', crs, (8, 4))



# --------------------------------------------------------------
# Z 軸で-137度回転（東経137度が手前に）
# Y 軸で  37度回転（北緯37度が赤道上の位置に持ってくる）
# X 軸で 135度回転
# Y 軸で -85度回転（回転中心を北緯85度の位置に持ってくる）
# --------------------------------------------------------------
r = Ry(-85) @ Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(min_latitude=-88, max_latitude=88),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig3', crs, (8, 8))



# --------------------------------------------------------------
# Z 軸で-143度回転（東経143度が手前に）
# Y 軸で  44度回転（北緯44度が赤道上の位置に持ってくる）
# X 軸で  35度回転
# Y 軸で -87度回転（回転中心を北緯87度の位置に持ってくる）
# --------------------------------------------------------------
r = Ry(-87) @ Rx(35) @ Ry(44) @ Rz(-143)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(min_latitude=-88, max_latitude=88),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig4', crs, (8, 8))



# --------------------------------------------------------------
# Z 軸で-137度回転（東経137度が手前に）
# Y 軸で  37度回転（北緯37度が赤道上の位置に持ってくる）
# X 軸で 135度回転
# Y 軸で -40度回転（回転中心を北緯40度の位置に持ってくる）
# --------------------------------------------------------------
r = Ry(-40) @ Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.LambertConformal(
            central_longitude=135,
            standard_parallels=(33, 45)),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
crs.set_extent([100, 170, 10, 60], use_base_crs=True)
plot_map('fig5', crs, (8, 8))



r = Rx(-15) @ Ry(36) @ Rz(-139)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
crs.set_extent([-20, 20, -10, 15], use_base_crs=True)
plot_map('fig11', crs, (8, 8))


r = Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(central_longitude=0.0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
#crs.set_extent([-30, 30, -25, 10], use_geodetic=True, use_base_crs=False)
plot_map('fig12', crs, (8, 8))


r = Ry(-50) @ Rx(-70) @ Ry(90) @ Rz(-120)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.LambertConformal(
            central_longitude=135,
            standard_parallels=(33, 45)),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
#crs.set_extent([-50, 50, 15, 60], use_geodetic=True, use_base_crs=False)
plot_map('fig5', crs, (8, 8))

r = Rx(135) @ Ry(35) @ Rz(-135)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig6', crs, (8, 8))

crs.set_extent([-2000000, 2000000, -2000000, 2000000], use_geodetic=False)
plot_map('fig7', crs, (8, 8))


r = Rz(0) @ Ry(0) @ Rz(0)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('sphere_1', crs, (8, 8))

r = Rz(0) @ Ry(0) @ Rz(-120)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('sphere_2', crs, (8, 8))

r = Rz(0) @ Ry(45) @ Rz(-120)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('sphere_3', crs, (8, 8))

r = Rz(60) @ Ry(45) @ Rz(-120)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('sphere_4', crs, (8, 8))

crs = GeneralObliqueProjection(
        ccrs.Miller(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig13', crs, (8, 8))

r = Rz(50) @ Ry(23.4) @ Rz(-135-60)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Orthographic(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('sphere_5', crs, (8, 8))


r = Rx(135) @ Ry(36.695) @ Rz(-137.211)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.AzimuthalEquidistant(central_longitude=0),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
crs.set_extent([-3000000, 3000000, -3000000, 3000000], use_geodetic=False)
plot_map('fig_20', crs, (8, 8))


r = Ry(0) @ Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Robinson(),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig_21', crs, (8, 4))


r = Ry(-85) @ Rx(135) @ Ry(37) @ Rz(-137)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(min_latitude=-89, max_latitude=89),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig_22', crs, (8, 8))


r = Ry(-87.5) @ Rx(35) @ Ry(44) @ Rz(-143)
params = params_from_rotation(r)
crs = GeneralObliqueProjection(
        ccrs.Mercator(min_latitude=-88.5, max_latitude=88.5),
        central_longitude=params['lon_0'],
        pole_latitude=params['lat_p'], pole_longitude=params['lon_p'])
plot_map('fig_23', crs, (8, 8))

