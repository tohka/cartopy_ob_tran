# General Oblique Transformation for CartoPy

## Usage

```
import cartopy.crs as ccrs
from ob_tran import GeneralObliqueProjection

crs = GeneralObliqueProjection(
        ccrs.Mollweide(),
        central_longitude=120,
        pole_latitude=40, pole_longitude=-55)
```
