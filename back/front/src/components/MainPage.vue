<template>
  <div class="wrapper_page">
    <main>
      <article class="wrapper_sections">
        <dir-chat></dir-chat>
        <dir-user-card></dir-user-card>
      </article>

      <article class="block-game wow bounceIn">
        <section class="block-game__section-settings">
          <h2 class="text-center">Настройки игры</h2>
          <fieldset>
            <form class="section-settings__form-settings" @submit="createGame">
              <label>
                Выберите уровень сложности
                <select required v-model="dataGame.lvlGame">
                  <option selected value="Легкий">Легкий</option>
                  <option value="Средний">Средний</option>
                  <option value="Выше среднего">Выше среднего</option>
                  <option value="Высокий">Высокий</option>
                </select>
              </label>
              <label>
                Напишите имя игры
                <input type="text" maxlength="10" v-model="dataGame.titleCustomGame" @input="validateNameCustomGame" required>
              </label>
              <button class="btn_def form-settings__btn-submit" title="Только для авторизованных пользователей" type="submit">
                <span> Создать игру</span>
                <i class="fa fa-gamepad" aria-hidden="true"></i>
              </button>
            </form>
          </fieldset>
          <hr>
        </section>
        <section class="block-game__section-list-game">
          <h2 class="text-center">Список игр</h2>
          <div class="section-list-game__template-game" v-for="game in listGames">
            <table class="table" data->
              <thead>
              <tr>
                <th scope="col">Название игры</th>
                <th scope="col">Количество участников</th>
                <th scope="col">Сложность</th>
                <th scope="col">Ник создателя</th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <td>{{ game.nameGame }}</td>
                <td>{{ game.countPlayers }}</td>
                <td>{{ game.lvlGame }}</td>
                <td>{{ game.userCreatedGame }}</td>
              </tr>
              </tbody>
            </table>
            <button title="Только для авторизованных пользователей"
                    type="button" class="btn btn_def template-game__btn-connect"
                    :data-uid-game="game.uidGame"
                    :data-name-game="game.nameGame"
                    @click="connectToGame">
              <i class="fa fa-users" aria-hidden="true"></i>
              <span>Присоединиться</span>
            </button>
          </div>
        </section>
      </article>
    </main>
    <footer>
      <div class="section-links">
        <a href="#">От разработчиков</a>
      </div>
      <div class="section-legal">
        2017 copyright
      </div>
    </footer>
  </div>
</template>

<style>

  footer {
    display: grid;
    grid-template-rows: 1fr 1fr;
    grid-template-columns: 1fr;
    grid-gap: 20px;

    background: rgb(66,66,66);
  }

  .section-links a {
    color: #8f8f8f;
  }

  .section-links a:hover {
    color: #e8e8e8;
  }

</style>



<script>

  export default {
    name: 'Lobby',
    data() {
      return {
        socket: null,
        textBanner: 'Сперва вам нужно авторизоваться',

        dataGame: {
          titleCustomGame: '',
          lvlGame: 'Легкий'
        },

        listGames: []
      }
    },
    created() {
      this.socket = this.$store.state.socket;
      // need fix auto log-in
      // this.socket.addEventListener('open', this.rememberUserData);
    },
    methods: {
      rememberUserData() {
        this.socket.removeEventListener('open', this.rememberUserData);
        if (localStorage.getItem('userDataForLogin')) {
          this.socket.addEventListener('message', this.getResponseFromServerWithAuth);
          this.socket.send(JSON.stringify(JSON.parse(localStorage.getItem('userDataForLogin'))));
        }
      },
      getResponseFromServerWithAuth(e) {
        const response = JSON.parse(e.data);
        if (response.type !== 'auth_error') {
          const userData = {
            loginSuccess: true,
            login: JSON.parse(localStorage.getItem('userDataForLogin')).data.user,
            avatar: 'https://thesocietypages.org/socimages/files/2009/05/vimeo.jpg',
            raiting: 0
          };
          this.$store.commit('setUserData', userData);
        }
        this.socket.removeEventListener('message', this.getResponseFromServerWithAuth);
      },
      validateNameCustomGame() {
        this.dataGame.titleCustomGame = this.dataGame.titleCustomGame.replace(/\W+/gi, '');
      },
      createGame(e) {
        e.preventDefault();
        if (!this.$store.state.userData.loginSuccess) return this.callAnimationBanner();
        const userCreatedGame = this.$store.state.userData.login;
        const nameGame = this.dataGame.titleCustomGame;
        const lvlGame = this.dataGame.lvlGame;
        const uidGame = parseInt(new Date().getTime()/1000);
        this.listGames.push({
          userCreatedGame,
          nameGame,
          lvlGame,
          uidGame,
          countPlayers: 1
        });
        // Уведомить сервер,что создалась игра
      },
      connectToGame(e) {
        if (!this.$store.state.userData.loginSuccess) return this.callAnimationBanner();
        this.$store.commit('setParticipantGame', true);
        this.$router.push({name: 'Game', params: {nameGame: `${e.currentTarget.dataset.nameGame}`}});
        // Уведомить сервер о том,что к данной игре подключились
        // Через e.target.uid можно узнать id game
      },
      getCurrentTime() {
        const date = new Date();
        const hours = date.getHours();
        const minutes = date.getMinutes() > 9 ? date.getMinutes() : `0${date.getMinutes()}`;
        const seconds = date.getSeconds() > 9 ? date.getSeconds() : `0${date.getSeconds()}`;
        return `${hours}:${minutes}:${seconds}`;
      },
      callAnimationBanner() {
        this.$store.commit('setAnimation', {
          run: true,
          textBanner: this.textBanner
        });
      }
    }
  }

</script>

<style scoped>

  .wrapper_page {
    display: grid;
    grid-template-rows: 10fr 1fr;
    grid-template-columns: 1fr;
  }

  main {
    display: grid;
    grid-template-rows: 100px 0.8fr minmax(1fr, 18fr);
    grid-template-columns: 1fr;
    grid-gap: 50px;
    background: #b8c6df; /* Old browsers */
    background: -moz-linear-gradient(top, #b8c6df 0%, #6d88b7 100%); /* FF3.6-15 */
    background: -webkit-linear-gradient(top, #b8c6df 0%,#6d88b7 100%); /* Chrome10-25,Safari5.1-6 */
    background: linear-gradient(to bottom, #b8c6df 0%,#6d88b7 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#b8c6df', endColorstr='#6d88b7',GradientType=0 ); /* IE6-9 */
    padding: 50px;
  }


  .block-game {
    display: grid;
    grid-template-rows: 1fr minmax(3fr, 18fr);
    grid-template-columns: 1fr;

    width: 70%;
    margin: 0 auto;
    padding: 10px;

    border: 1px solid gray;
    border-radius: 5px;
    background: rgb(242,246,248); /* Old browsers */
    background: -moz-linear-gradient(top, rgba(242,246,248,1) 0%, rgba(224,239,249,1) 100%, rgba(224,239,249,1) 100%, rgba(181,198,208,1) 100%); /* FF3.6-15 */
    background: -webkit-linear-gradient(top, rgba(242,246,248,1) 0%,rgba(224,239,249,1) 100%,rgba(224,239,249,1) 100%,rgba(181,198,208,1) 100%); /* Chrome10-25,Safari5.1-6 */
    background: linear-gradient(to bottom, rgba(242,246,248,1) 0%,rgba(224,239,249,1) 100%,rgba(224,239,249,1) 100%,rgba(181,198,208,1) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#f2f6f8', endColorstr='#b5c6d0',GradientType=0 ); /* IE6-9 */
  }

  .block-game__section-settings {
    -moz-border-radius-topleft: 5px;
    -moz-border-radius-topright: 5px;
   }

  .section-settings__form-settings {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
    margin: 10px;
  }

  .block-game__section-settings label {
    margin-bottom: 0;
  }

  .form-settings__btn-submit {
    display: flex;
    justify-content: space-around;
    align-items: center;


    font-size: 24px;
  }

  .block-game__section-list-game {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;

    padding: 5px;

    font-weight: bold;
  }

  .section-list-game__template-game {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 4fr 1fr;

    min-height: 75px;
    margin: 10px;

    border: 1px solid black;
    border-radius: 3px;
  }

  th {
    color: green;
  }

  td {
    color: red;
  }

  .template-game__btn-connect {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .template-game__btn-connect .fa {
    margin-right: 15px;
  }



  .разделМеждуСекциями {}

  .wrapper_sections {
    display: grid;
    grid-template-rows: minmax(300px, 500px);
    grid-template-columns: 3fr minmax(300px, 360px);
    grid-gap: 20px;
  }






</style>

<style>

  .fa {
    font-size: 22px;
  }

  .fa-gamepad {
    font-size: 25px;
    margin-left: 5px;
  }

  button {
    cursor: pointer;
  }


</style>
