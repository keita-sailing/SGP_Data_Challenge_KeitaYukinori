

const timearray = source_origin.data.time
var startindex = timearray.findIndex(
    (time) => time > cb_obj.value-60000)
var endindex = timearray.findIndex(
    (time) => time > cb_obj.value+60000)
const centerid = timearray.findIndex(
    (time) => time == cb_obj.value)

//Create list of showing track
const longitude = source_origin.data[`${country}_LONGITUDE_merc`].slice(startindex, endindex)
const latitude = source_origin.data[`${country}_LATITUDE_merc`].slice(startindex, endindex)

//Create list of mark positions
var mark_x = []
var mark_y = []
for (const mark of marktypes) {
    mark_x.push(source_origin.data[`${mark}_LONGITUDE_merc`][centerid])
    mark_y.push(source_origin.data[`${mark}_LATITUDE_merc`][centerid])
}


//culculate current position and speed
const current_lat = source_origin.data[`${country}_LATITUDE_merc`][centerid]
const current_lng = source_origin.data[`${country}_LONGITUDE_merc`][centerid]

const label_texts = []
const key_list = ['windward', 'leeward', 'port', 'starboard']
for (const key of key_list){
    const pushtext = `Ride Height ${key}: ` + source_origin.data[`LENGTH_RH_${key}`][centerid].toString() + 'mm'
    label_texts.push(pushtext)
}

tracline.data = { longitude: longitude, latitude: latitude }
markposi.data = { x: mark_x, y: mark_y }
boatposi.data = { x: [current_lng], y: [current_lat] }
for (var i=0; i<4; i++){
    labels[i].x = current_lng
    labels[i].y = current_lat
    labels[i].text = label_texts[i]
}