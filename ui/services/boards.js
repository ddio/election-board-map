import boardData from '@/../datas/boards.json'

const api = {
  imagePrefix: 'https://www.readr.tw/proj-assets/election-board/uploads/images/',
  get (id) {
    return boardData[id]
  },
  all () {
    return boardData
  },
  image (imageName) {
    return imagePrefix + imageName
  }
}

export default api
