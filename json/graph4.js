const timearray = source.data.time

var startindex = timearray.findIndex(
    (time) => time > cb_obj.value-60000)
var endindex = timearray.findIndex(
    (time) => time > cb_obj.value+60000)
const centerid = timearray.findIndex(
    (time) => time == cb_obj.value)

//Create list of showing track
const longitude = source.data.AUS_LONGITUDE_merc.slice(startindex, endindex)
const latitude = source.data.AUS_LATITUDE_merc.slice(startindex, endindex)

//Create list of mark positions
var mark_x = []
var mark_y = []
for (const mark of marktypes) {
    mark_x.push(source.data[`${mark}_LONGITUDE_merc`][centerid])
    mark_y.push(source.data[`${mark}_LATITUDE_merc`][centerid])
}

//Create list of boat position
var boat_x = []
var boat_y = []
var dist2finish = []
for (const country of countrylist) {
    boat_x.push(source.data[`${country}_LONGITUDE_merc`][centerid])
    boat_y.push(source.data[`${country}_LATITUDE_merc`][centerid])
    dist2finish.push(country + ': ' + source.data[`${country}_Distance2Leader`][centerid].toString() + 'm')
}

//set new data
tracline.data = { AUS_LONGITUDE_merc: longitude, AUS_LATITUDE_merc: latitude }
markposi.data = { x: mark_x, y: mark_y }
boatposi.data = { x: boat_x, y: boat_y }
labels.source.data = { x: boat_x, y: boat_y, text: dist2finish }