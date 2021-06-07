from app4R import models


def GetRate(points):

    rate = models.PointsToMoneyConversionRate.objects.first()
    return points * rate.points
