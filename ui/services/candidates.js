import datas from '@/../datas/candidates.json'

const api = {
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
