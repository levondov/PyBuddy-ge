from items import Item
import datetime

# create an object with item id 383
myitem = Item(385)

# grab current price data
myitem.guidePrice()

# grab price data from may 2nd 2017 at 5:30:03pm , and 3 milliseconds
myitem.guidePrice(date=datetime.datetime(2017,5,2,17,30,03,3))

# plot data from the last 6 hours in 30 minute intervals
time6hoursago = datetime.datetime.now() - datetime.timedelta(hours=6)
myitem.graph(g=30,start=time6hoursago)

