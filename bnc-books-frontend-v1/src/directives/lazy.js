import { lazyLoad } from '@/utils/performance'

export default {
  install(app) {
    app.directive('lazy', lazyLoad)
  }
}