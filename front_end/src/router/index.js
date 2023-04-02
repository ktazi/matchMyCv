import Vue from 'vue'
import VueRouter from 'vue-router'
import NewAdvert from '../components/NewAdvert'
import SelectAdvert from '../components/SelectAdvert'
import ImportCV from '../components/ImportCV'
import ScoreAffichage from '../components/ScoreAffichage'
import NoteCV from '../components/NoteCV'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: SelectAdvert
  },
  {
    path: '/new',
    name: 'new',
    component: NewAdvert
  },
  {
    path : '/modifAnnonce/:id',
    name : 'modif',
    component : ImportCV
  },
  {
    path: '/score/:id',
    name : 'score',
    component : ScoreAffichage
  },
  {
    path:'/note/:idannonce/:numcv',
    name : 'note',
    component : NoteCV
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
