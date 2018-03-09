<template>
  <section class="section__user-card wow fadeInRight">
    <h3 class="user-card__title"><i class="fa fa-id-card" aria-hidden="true"></i> Карточка пользователя</h3>
    <div class="user-card__avatar-box">
      <img class="avatar-box__img" :src="$store.state.userData.avatar" alt="avatar-user">
    </div>
    <span class="user-card__template-info">
      Ваш ник:
      <span class="text-success"> {{ $store.state.userData.login}} </span>
    </span>
    <span class="user-card__template-info">Статус: <span class="text-success">Online</span></span>
    <span class="user-card__template-info" >Вход выполнен: <span :class="$store.state.userData.loginSuccess === true
     ? ' text-success'
     : 'text-danger'"> {{ $store.state.userData.loginSuccess === true ? 'Да' : 'Нет'}} </span>
    </span>
    <span class="user-card__template-info">
      <span>Текущий рейтинг: </span>
      <span class="text-success"> {{ $store.state.userData.raiting }} </span>
    </span>
    <label>Сменить аватар:
      <input type="file" value="Сменить аватар" accept="image/*" @change="avatarLoaded">
    </label>
    <button class="btn btn_def"
            @click="logOut">
      <span>Выйти с аккаунта</span>
      <i class="fa fa-arrow-alt-square-right"></i>
    </button>


  </section>
</template>


<script>
  export default {
    name: 'userCard',
    data() {
      return {
        socket: null
      }
    },
    created() {
      this.socket = this.$store.state.socket;
    },

    methods: {
      avatarLoaded(e) {
        this.getImgFileWithReader(e)
        .then((img) => {
          this.$store.commit('setAvatar', img);
        });

      },
      logOut() {
        this.$store.commit('setDefaultUser');
      },
      getImgFileWithReader(e) {
        return new Promise((done) => {
          const fileImg = e.target.files[0];
          const reader  = new FileReader();

          reader.onloadend = function () {
            done(reader.result)
          };
          if (fileImg) reader.readAsDataURL(fileImg);
        })
      }
    }
  }

</script>


<style scoped>

  .section__user-card {
    padding: 15px;

    border: 1px solid green;
    border-radius: 10px;
    background: rgb(242,246,248); /* Old browsers */
    background: -moz-linear-gradient(top, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 10%, rgba(181,198,208,1) 100%, rgba(224,239,249,1) 100%); /* FF3.6-15 */
    background: -webkit-linear-gradient(top, rgba(242,246,248,1) 0%,rgba(216,225,231,1) 10%,rgba(181,198,208,1) 100%,rgba(224,239,249,1) 100%); /* Chrome10-25,Safari5.1-6 */
    background: linear-gradient(to bottom, rgba(242,246,248,1) 0%,rgba(216,225,231,1) 10%,rgba(181,198,208,1) 100%,rgba(224,239,249,1) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#f2f6f8', endColorstr='#e0eff9',GradientType=0 ); /* IE6-9 */
    box-shadow: 11px 11px 29px -11px #000000;
  }

  .user-card__title {
    display: flex;
    justify-content: center;
    align-items: flex-end;

    margin-bottom: 25px;

    text-align: center;
    text-decoration: underline;
    font-weight: 700;
    font-size: 21px;
  }

  .user-card__avatar-box {
    display: flex;
    justify-content: center;
    align-items: center;

    width: 170px;
    height: 170px;
    margin: 25px 20%;

    border: 2px solid #a3cc3e;
    border-radius: 50%;
  }

  .avatar-box__img {
    width: 140px;
    height: 140px;
    margin: 5px;

    border-radius: 50%;
    border: 2px solid gray;
  }

  .user-card__template-info {
    display: block;

    margin: 10px 0;

    font-weight: bold;
    font-size: 16px;
  }

  .fa-id-card {
    font-size: 25px;
    margin-right: 5px;
  }




</style>

