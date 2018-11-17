import boardData from '@/../datas/boards.json'
import _ from 'lodash'
/*

Example data:
[
  "668": {
    "image": "1541522321-af5e424f73abcca7e72e57665cf8dc0b.jpg",
    "candidates": [
      34181
    ],
    "county": "台北市",
    "verified_amount": 0,
    "road": "台9線134號",
    "district": "文山區",
    "coordinates": [
      24.997083333333336,
      121.54076388888889
    ],
    "id": 668
  }
]

*/

const api = {
  imagePrefix: 'https://www.readr.tw/proj-assets/election-board/uploads/images/',
  get (id) {
    return boardData[id]
  },
  all () {
    return boardData
  },
  image (imageName) {
    return api.imagePrefix + imageName
  }
}

export default api
