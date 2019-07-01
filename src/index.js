"use strict";

// import "@babel/polyfill";
import "core-js/stable";
import "regenerator-runtime/runtime";

import "element-ui/lib/theme-chalk/index.css";
import "assets/global-styles.scss";

import Vue from "vue";

import VueScrollTo from "vue-scrollto";
Vue.use(VueScrollTo);

import {
    Form,
    FormItem,
    Pagination,
    Table,
    TableColumn,
    Card,
    Select,
    Option,
    Input,
    Button
} from "element-ui";
import lang from "element-ui/lib/locale/lang/en";
import locale from "element-ui/lib/locale";
locale.use(lang);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Pagination);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Card);
Vue.use(Select);
Vue.use(Option);
Vue.use(Input);
Vue.use(Button);

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
Vue.component("font-awesome-icon", FontAwesomeIcon);

import { library, config } from "@fortawesome/fontawesome-svg-core";
config.autoReplaceSvg = "nest";
import { faMinusSquare, faPlusSquare } from "@fortawesome/pro-light-svg-icons";
library.add(faMinusSquare, faPlusSquare);

import App from "components/app.vue";
import { router } from "./routes";
import { store } from "store";

App.router = router;
App.store = store;
const app = new Vue(App);
