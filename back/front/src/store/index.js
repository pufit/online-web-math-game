import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    modePage: '',
    socket: null,

    nameControlButton: 'Главная',

    userData: {
      loginSuccess: false,
      login: 'Прохожий',
      avatar: 'https://thesocietypages.org/socimages/files/2009/05/vimeo.jpg',
      raiting: 0
    },

    rightStartGame: false,
    participantGame: false,

    gameStarted: false,

    animated: {
      run: false,
      textBanner: ''
    }
  },
  mutations: {
    setDefaultUser(state) {
      state.userData = {
        loginSuccess: false,
        login: 'Прохожий',
        avatar: 'https://thesocietypages.org/socimages/files/2009/05/vimeo.jpg',
        raiting: 0
      };
    },
    setModePage(state, strValue) {
      state.modePage = strValue;
    },
    setUserData(state, obj) {
      state.userData = obj;
    },
    setConnectFromServer(state, objConnect) {
      state.socket = objConnect;
    },
    setStateGame(state, boolValue) {
      state.gameStarted = boolValue;
    },
    setParticipantGame(state, boolValue) {
      state.participantGame = boolValue;
    },
    setNameControlButton(state, strValue) {
      state.nameControlButton = strValue;
    },
    setAnimation(state, obj) {
      state.animated = obj;
    },
    setAvatar(state, base64Img) {
      state.userData.avatar = base64Img;
    }
  }
})
