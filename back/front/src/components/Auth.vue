<template>
  <main>
    <div class="container">
      <div class="main__section section_center">
        <div class="section__main-auth wow fadeInDownBig">
          <h2 class="main-auth__title text-effect-shadow">
              {{ $store.state.modePage === 'login' ? 'Sign to MarhV2' : 'Join to MarhV2' }}
          </h2>
          <form class="main-auth__form" @submit.prevent="authorization">
            <label for="login">Login</label>
            <input type="text" class="margin-bot-md" id="login" v-model="userData.login" required autofocus>
            <label for="password">Password</label>
            <input type="password" class="margin-bot-md" id="password" v-model="userData.pass" required>

            <div class="alert alert-danger margin-bot-lg" role="alert" v-if="errorAuth">
              {{ messageError }}
            </div>
            <button type="submit" class="btn form__btn-submit margin-top-md">
                {{ $store.state.modePage === 'login' ? 'Войти на сайт' : 'Зарегистрироваться' }}
            </button>
          </form>
          <div class="main-auth__footer margin-bot-lg">
            <span> {{ $store.state.modePage === 'login' ? 'New to MarhV2?': 'Registered on MarhV2?'}} </span>
            <a href="#" @click.prevent="getAnotherPage">
                {{ $store.state.modePage === 'login' ? 'Create a account': 'Sign in account.' }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>




<script>
  import * as firebase from 'firebase';

  export default {
    name: 'AuthPage',
    data: () => {
      return {
        modePage: '',
        socket: null,

        userData: {
          login: '',
          pass: '',
        },

        messageError: '',
        errorAuth: false,
      }
    },
    created () {
      this.setModePage();
      this.socket = this.$store.state.socket;
    },
    watch: {
      '$route': 'setModePage',
      '$store.state.modePage': function () {
        this.errorAuth = false;
        this.messageError = '';
      }
    },
    methods: {
      setModePage() {
        console.log(this.$route);
        this.modePage = this.$route.params.modePage;
        this.$store.commit('setModePage', this.modePage);
      },
      getAnotherPage () {
        let path;
        if (this.modePage === 'login') {
          path = {name: 'Auth', params: {modePage: 'registration'}};
        } else {
          path = {name: 'Auth', params: {modePage: 'login'}};
        }
        this.$router.push(path);
      },
      authorization() {
        const requestType = this.modePage === 'registration' ? 'reg' : 'auth';

        this.socket.send(JSON.stringify({
          type: requestType,
          data: {
            'user': this.userData.login,
            'password': this.userData.pass
          }
        }));
        this.socket.addEventListener('message', this.getResponseFromServerWithAuth);
      },
      getResponseFromServerWithAuth(e) {
        const response = JSON.parse(e.data);
        console.log(response);
        if (response.type === 'auth_error' || response.type === 'reg_error') {
          this.messageError = response.data;
          this.errorAuth = true;
        } else {
          this.$router.push({name: 'Lobby'});
          const userData = {
            loginSuccess: true,
            login: this.userData.login,
            avatar: 'https://thesocietypages.org/socimages/files/2009/05/vimeo.jpg',
            raiting: 0
          };
          this.$store.commit('setUserData', userData);
          // localStorage.setItem('userDataForLogin', JSON.stringify({
          //   type: 'auth',
          //   data: {
          //     'user': this.userData.login,
          //     'password': this.userData.pass
          //   }
          // }));
          this.errorAuth = false;
        }
        this.socket.removeEventListener('message', this.getResponseFromServerWithAuth);
      },
    }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>



  .text-effect-shadow {
    color: transparent;
    text-shadow: rgba(255, 255, 255, 0.5) 0 3px 3px;
    background-color: #666666;

    -webkit-background-clip: text;
  }

  .margin-bot-sm {
    margin-bottom: 10px;
  }

  .margin-bot-md {
    margin-bottom: 20px;
  }

  .margin-bot-lg {
    margin-bottom: 30px;
  }

  .margin-top-md {
    margin-top: 20px;
  }


  main {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;


    border: 2px solid black;
    -moz-border-radius-bottomleft: 5px;
    -moz-border-radius-bottomright: 5px;
    background: #2b3237;
  }


  .section_center {
    position: relative;

    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    flex-flow: row;
    justify-content: center;

    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    -ms-flex-flow: row;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
  }

  .section__main-auth {
    width: 30%;
  }

  .main-auth__form {
    position: relative;

    padding: 20px;
    margin: 15px 0;

    border: 1px solid #d8dee2;
    border-radius: 5px;
    background: #fafbfc;
  }

  .main-auth__title {
    color: darksalmon;
    text-align: center;
  }


  .main-auth__form input {
    min-height: 34px;
    line-height: 34px;

    padding: 6px 8px;
    border: 1px solid #d1d5da;
    border-radius: 3px;
  }
  .main-auth__form label {
    margin-bottom: 3px;
  }
  .main-auth__form label, .main-auth__form input {
    display: block;
    width: 100%;
  }
  .main-auth__form .secondary-controls {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    justify-content: flex-start;

    -webkit-box-pack: start;
    -ms-flex-pack: start;
    -webkit-box-align: center;
    -ms-flex-align: center;

    align-items: center;
  }



  .main-auth__footer {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    justify-content: space-around;

    width: 100%;
    padding: 13px 15px;
    font-size: 14px;

    border: 1px solid #d8dee2;
    border-radius: 5px;
    background: #f9f9f9;
  }

  .form__btn-submit {
    position: relative;

    width: 100%;
    min-height: 35px;

    border-radius: 3px;
    border: 0;
    color: white;
    cursor: pointer;
    overflow: hidden;
    background: #26a69b;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, .4);
  }

  .form__btn-submit:after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 5px;
    height: 5px;
    background: rgba(255, 255, 255, .5);
    opacity: 0;
    border-radius: 100%;
    transform: scale(1, 1) translate(-50%);
    transform-origin: 50% 50%;
  }

  .form__btn-submit:hover, form__btn-submit:active, form__btn-submit:focus {
    background: #2bbbae;
  }

  .form__btn-submit:focus:not(:active)::after {
    animation: ripple 0.8s ease-out;
  }

</style>
