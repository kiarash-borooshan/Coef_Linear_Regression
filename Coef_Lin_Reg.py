import gdal
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.style.use("dark_background")

path = ""
name = "«LST_B10.tif" """ stackesd LST image with 15 layers"""
path_name = path + name
outFileName = path + "Coef_LinReg" + name

""" read data """
ds = gdal.Open(path_name)
Arys = ds.ReadAsArray()
output = np.zeros((ds.RasterYSize, ds.RasterXSize))


""" Reg Process """
""" ref: https://realpython.com/linear-regression-in-python/ """

""" linear Reg for one pixel"""
# x = np.array([1, 2, 3, 4, 5, 6, 7,
#               8, 9, 11, 12, 13, 14, 15]).reshape(-1, 1)
#
# vlue = []
# for i in range(0, 7):
#     vlue.append(Arys[i, 24, 0])
# y = np.array(vlue)
#
# LinReg = LinearRegression().fit(x, y)
#
# """ print result"""
# y_pred = LinReg.predict(x)
#
# r_sq = LinReg.score(x, y)
# print('coefficient of determination:', r_sq)
#
# print("intercept: ", LinReg.intercept_)
# print("slope: ", LinReg.coef_)
#
#
# """ plot """
# plt.plot(x, y, "ro")
# plt.plot(x, y_pred)
# plt.title("linear regression for one pixel \n"
#           " of LST time series")
# label_tick = ["1398-12-05", "1398-12-14", "1398-12-21", "1399-01-01",
#               "1399-01-08", "1399-01-17", "1399-01-24", "1399-11-24",
#               "1399-12-08", "1399-12-17", "1399-12-24", "1400-01-03",
#               "1400-01-10", "1400-01-19", "1400-01-26"]
# plt.xticks(x, label_tick, rotation=35)
# plt.xlabel("date")
# plt.ylabel("LST")


""" Linear Reg for all pixels """
for i in range(ds.RasterYSize):
    for j in range(ds.RasterXSize):

        """ if value is nan """
        if np.isnan(Arys[1, i, j]):
            output[i, j] = Arys[1, i, j]
            continue

        else:
            x = np.array([1, 2, 3, 4, 5, 6, 7,
                          8, 9, 11, 12, 13, 14, 15]).reshape(-1, 1)

            vlue = []
            for ii in range(7, 15):
                vlue.append(Arys[ii, i, j])
            y = np.array(vlue)

            del vlue

            LinReg = LinearRegression().fit(x, y)

            output[i, j] = LinReg.coef_


""" write export """
driver = gdal.GetDriverByName("GTiff")
outputDS = driver.Create(outFileName,
                         ds.RasterXSize,
                         ds.RasterYSize,
                         1,
                         eType=ds.GetRasterBand(1).DataType)
outputDS.SetGeoTransform(ds.GetGeoTransform())
outputDS.SetProjection(ds.GetProjection())
outband = outputDS.GetRasterBand(1).WriteArray(output)

outputDS.FlushCache()
del outputDS, ds

print("finish")
