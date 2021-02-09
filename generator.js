//const dotenv = require('dotenv');
const util = require('util');
const fs = require('fs');
const csv = require('csv');
const CSVDIR = './test-csv-data';
const NUMOFCAM = 10;
const NUMOFDATA = 10;
//dotenv.config();
fs.mkdir(CSVDIR,(error,output)=>{
    console.log(output);
});
async function main() {
    for (var i=0; i <= NUMOFCAM; i++) {
        const macaddress = toHex(Math.floor(Math.random() * (16 ** 12)));
        //const macaddress = i;
        fs.mkdir(CSVDIR + '/' + macaddress,(error,output)=>{});
        for(var frame_number=0; frame_number <= NUMOFDATA; frame_number++) {
            let num = Math.floor(Math.random() * 27000) + 27000;
            let filepath = CSVDIR + '/' + macaddress + '/' + frame_number + '.csv';
            let data = createDummyData(num, i);
            const output = await util.promisify(csv.stringify)(data);
            await util.promisify(fs.writeFile)(filepath, output);
            console.log(filepath);
        };
    }
}
function createDummyData(num, offset) {
    let raw_data = [];
    for(var i=offset; i < num + offset; i++) {
        const x = i + 0.12345;
        const y = i + 0.12345;
        const z = i + 0.12345;
        raw_data.push([x,y,z]);
    }
    return raw_data;
}
function toHex(v) {
    return (('000000000000' + v.toString(16).toUpperCase()).substr(-12));
}
main();
