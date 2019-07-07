"use strict";

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import { processFolder } from "./data-loader.service";

const configuration = {
    strict: process.env.NODE_ENV !== "production",
    state: reset(),
    mutations: {
        saveIndex(state, payload) {
            state.index = [...payload.index];
        },
        setSelectedFolder(state, payload) {
            state.selectedFolder = { ...payload };
        },
        setProcessingStatus(state, payload) {
            state.processing = { ...payload };
        },
        storeIndex(state, payload) {
            state.index = [...payload];
        }
    },
    actions: {
        async processFolder({ state, commit }) {
            commit("storeIndex", []);
            await new Promise(resolve => {
                setTimeout(resolve, 200);
            });
            await processFolder({ folder: state.selectedFolder, commit });
        }
    },
    getters: {}
};
export const store = new Vuex.Store(configuration);

function reset() {
    return {
        index: [],
        selectedFolder: {},
        processing: {
            current: undefined,
            total: undefined,
            file: undefined
        }
    };
}
