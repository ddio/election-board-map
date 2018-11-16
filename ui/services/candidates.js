import datas from '@/../datas/candidates.json'

/*

Example data:
[
  "65532": {
    "district": null,
    "county": "桃園市",
    "name": "蘇世岳",
    "party": "無黨籍",
    "image": "",
    "number": null,
    "type": "councilors",
    "boards_set": [
      493
    ],
    "id": 65532,
    "candidate": 65532
  }
]

*/

const api = {
  type: {
    MAYORS: 'mayors',
    COUNCILORS: 'councilors'
  },
  get (id) {
    return datas[id]
  },
  find (ids) {
    return ids.map(id => datas[id])
  },
  all () {
    return datas
  }
}

export default api
