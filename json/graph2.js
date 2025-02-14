

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
const current_cog = source_origin.data[`${country}_GPS_COG`][centerid]
const current_sog = source_origin.data[`${country}_GPS_SOG`][centerid]
var label_text = ['VMC: ' + source_origin.data[`${country}_VMC`][centerid].toString() + 'km/h']//VMC


//culcurate arrow direction
var rad = current_cog * (Math.PI / 180)
var dN = Math.cos(rad) * current_sog * 5
var dE = Math.sin(rad) * current_sog * 5
const new_lat = current_lat+dN
const new_lng = current_lng+dE


//culcurate arrow direction
var rad_vmc = source_origin.data[`${country}_Mark_Angle`][centerid] * (Math.PI / 180)
var dN = Math.cos(rad_vmc) * source_origin.data[`${country}_VMC`][centerid] * 5
var dE = Math.sin(rad_vmc) * source_origin.data[`${country}_VMC`][centerid] * 5
const vmc_lat = current_lat+dN
const vmc_lng = current_lng+dE


tracline.data = { longitude: longitude, latitude: latitude }
markposi.data = { x: mark_x, y: mark_y }
boatposi.data = { x: [current_lng], y: [current_lat] }
labels.source.data = { x: [vmc_lng], y: [vmc_lat], text: label_text }
arrow.data = { x0: [current_lng], y0: [current_lat], x1: [new_lng], y1: [new_lat] }
head.data = { x: [new_lng], y: [new_lat], angle:[Math.PI*2 - rad] }
if(source_origin.data[`${country}_VMC`][centerid] > 0) {
    vmc_arrow.data = { x0: [current_lng], y0: [current_lat], x1: [vmc_lng], y1: [vmc_lat] }
    vmc_head.data = { x: [vmc_lng], y: [vmc_lat], angle: [Math.PI*2 - rad_vmc] }
} else {
    vmc_arrow.data = { x0: [vmc_lng], y0: [vmc_lat], x1: [current_lng], y1: [current_lat] }
    vmc_head.data = { x: [current_lng], y: [current_lat], angle: [Math.PI*2 - rad_vmc] }
}