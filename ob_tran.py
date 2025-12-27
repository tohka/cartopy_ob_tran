import numpy as np
import cartopy.crs as ccrs
import shapely.geometry as sgeom

class GeneralObliqueProjection(ccrs.Projection):
    _wrappable = True
    #_handles_ellipses = False

    def __init__(self, base_crs, central_longitude=None,
                 # New pole: `o_lon_p` / `o_lat_p`
                 pole_longitude=None, pole_latitude=None,
                 # Rotate about point: `o_alpha` / `o_lon_c` / `o_lat_c`
                 axis_azimuth=None,
                 rotation_center_longitude=None, rotation_center_latitude=None,
                 # New equator points: `o_lon_1` / `o_lat_1` / `o_lon_2` / `o_lat_2`
                 point1_longitude=None, point1_latitude=None,
                 point2_longitude=None, point2_latitude=None,
                 false_easting=None, false_northing=None, globe=None):
        """
        Initialize a general oblique transformation projection.

        This projection applies an oblique transformation to a base projection,
        allowing for various types of rotations and transformations of the
        coordinate system.

        Parameters
        ----------
        base_crs : cartopy.crs.Projection
            The base projection to apply the oblique transformation to.
        central__longitude : float, optional
            Central longitude in the rotated coordinate system (lon_0).
            Default is None.

        Oblique Transformation Methods (use one of the following):
        ---------------------------------------------------------
        New Pole Method:
            pole_longitude, pole_latitude: float, optional
                Longitude and latitude of the new pole (o_lon_p, o_lat_p).

        Rotation About Point Method:
            axis_azimuth : float, optional
                Azimuth of the rotation axis in degrees (o_alpha).
            rotation_center_longitude, rotation_center_latitude: float, optional
                Longitude and latitude of the rotation center (o_lat_c, o_lon_c).

        New Equator Points Method:
            point1_longitude, point1_latitude: float, optional
                Longitude and latitude of the first point on the new equator.
            point2_longitude, point2_latitude: float, optional
                Longitude and latitude of the second point on the new equator.

        General Parameters:
        ------------------
        false_easting : float, optional
            False easting in meters (x_0). Default is None.
        false_northing : float, optional
            False northing in meters (y_0). Default is None.
        globe : cartopy.crs.Globe, optional
            A Globe instance. If None, the base_crs's globe is used.

        Notes
        -----
        The projection requires exactly one of the following parameter sets:
        - pole_longitude and pole_latitude (New Pole Method)
        - axis_azimuth, rotation_center_longitude, and rotation_center_latitude (Rotation About Point Method)
        - point1_longitude, point1_latitude, point2_longitude, and point2_latitude (New Equator Points Method)

        If none of these sets are provided or an incomplete set is provided,
        a ValueError will be raised.
        """

        self.base_crs = base_crs 
        
        proj4_params = dict([
            ('proj', 'ob_tran'),
            ('o_proj', self.base_crs.proj4_params['proj']),
            ('units', 'm'),
        ])

        if pole_longitude is not None and pole_latitude is not None:
            # New pole
            proj4_params['o_lon_p'] = pole_longitude
            proj4_params['o_lat_p'] = pole_latitude
        elif (
            axis_azimuth is not None 
            and rotation_center_longitude is not None 
            and rotation_center_latitude is not None
        ):
            # Rotate about point
            proj4_params['o_alpha'] = axis_azimuth
            proj4_params['o_lon_c'] = rotation_center_longitude
            proj4_params['o_lat_c'] = rotation_center_latitude
        elif (
            point1_longitude is not None 
            and point1_latitude is not None 
            and point2_longitude is not None 
            and point2_latitude is not None
        ):
            # New equator points
            proj4_params['o_lon_1'] = point1_longitude
            proj4_params['o_lat_1'] = point1_latitude
            proj4_params['o_lon_2'] = point2_longitude
            proj4_params['o_lat_2'] = point2_latitude
        else:
            # Invalid argument combination
            raise ValueError("Invalid combination of arguments for GeneralObliqueProjection.")

        if central_longitude is not None:
            proj4_params['lon_0'] = central_longitude
        if false_easting is not None:
            proj4_params['x_0'] = false_easting
        if false_northing is not None:
            proj4_params['y_0'] = false_northing

        proj4_params = dict(self.base_crs.proj4_params) | proj4_params

        proj4_params = list(proj4_params.items())
        if globe is None:
            globe = self.base_crs.globe
        #globe = ccrs.Globe(
        #    semimajor_axis=globe.semimajor_axis,
        #    semiminor_axis=globe.semimajor_axis,
        #    ellipse=None
        #)
        super().__init__(proj4_params, globe=globe)

        self.threshold = self.base_crs.threshold
        self._x_limits = self.base_crs.x_limits
        self._y_limits = self.base_crs.y_limits
        self._boundary = self.base_crs.boundary

    def set_extent(self, extent, use_geodetic=True, use_base_crs=None):
        """
        Set the extent of the projection.

        Parameters
        ----------
        extent : tuple
            The extent of the projection in the form (lonmin, lonmax, latmin, latmax)
            or (xmin, xmax, ymin, ymax).
        use_geodetic : bool, optional
            If True, the extent is in geodetic coordinates. Defaults to True.
        use_base_crs : bool, optional
            If True, the extent is in the base projection. Defaults to None.
        """

        if use_geodetic:
            # extent : (lonmin, lonmax, latmin, latmax)
            if use_base_crs is None:
                # if `use_base_crs` is not specified, use base_crs
                use_base_crs = True

            lonmin, lonmax, latmin, latmax = extent

            n = 91
            lons = np.empty(4*n+1)
            lats = np.empty(4*n+1)
            lons[0*n:1*n] = np.full(n, lonmin)
            lons[1*n:2*n] = np.linspace(lonmin, lonmax, n, endpoint=False)
            lons[2*n:3*n] = np.full(n, lonmax)
            lons[3*n:4*n] = np.linspace(lonmax, lonmin, n, endpoint=False)

            lats[0*n:1*n] = np.linspace(latmin, latmax, n, endpoint=False)
            lats[1*n:2*n] = np.full(n, latmax)
            lats[2*n:3*n] = np.linspace(latmax, latmin, n, endpoint=False)
            lats[3*n:4*n] = np.full(n, latmin)

            lons[-1] = lons[0]
            lats[-1] = lats[0]

            if use_base_crs:
                #points = self.base_crs.transform_points(
                points = self.transform_points(
                        self.base_crs.as_geodetic(), lons, lats)
            else:
                points = self.transform_points(
                        self.as_geodetic(), lons, lats)

            self._boundary = sgeom.LinearRing(points)
            mins = np.min(points, axis=0)
            maxs = np.max(points, axis=0)
            self._x_limits = (mins[0], maxs[0])
            self._y_limits = (mins[1], maxs[1])

        else:
            # extent : (xmin, xmax, ymin, ymax)
            if use_base_crs is None:
                # if `use_base_crs` is not specified, oblique projection is used
                use_base_crs = False

            xmin, xmax, ymin, ymax = extent
            if use_base_crs:
                # base_crs (x, y) -> base_crs (lon, lat) -> oblique projection (x, y)
                # TODO
                None
            else:
                self._boundary = sgeom.LinearRing(
                        [(xmin, ymin), (xmin, ymax), (xmax, ymax),
                         (xmax, ymin), (xmin, ymin)])
                self._x_limits = (xmin, xmax)
                self._y_limits = (ymin, ymax)

    @property
    def boundary(self):
        return self._boundary

    @property
    def x_limits(self):
        return self._x_limits

    @property
    def y_limits(self):
        return self._y_limits


