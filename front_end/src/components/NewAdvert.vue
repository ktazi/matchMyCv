<template>
    <div class="container" id="formulaire">
            <h1 class="display-3 mt-4 mb-4"> Saisie annonce :</h1>
            <form>
                <div class="form-group">
                  <label for="annonce_name">Nom de l'emploi</label>
                  <input type="text" class="form-control" id="annonce_name" placeholder="Nom du poste" v-model="nom_annonce">
                </div>
                <div class="form-group">
                  <label for="annonce_name">Nom de l'employeur</label>
                  <input type="text" class="form-control" id="employeur_name" placeholder="Nom de l'employeur" v-model="nom_employeur">
                </div>
                <div class="row">
                    <div class="col-sm">
                        <label for="skillob">Skills obligatoires</label> 
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom compétence" id="skillob" v-model="inp_ob">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="add_elem(skill_ob, inp_ob)">Ajout</button>
                            </div>
                        </div>
                        <ul class="list-group" >
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillo, index) in skill_ob">
                              {{skillo}}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_ob,index)">-</span>
                            </li>
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_ob">Nombre points</label>
                            <input id="percentage_ob" type="number" v-model="score_ob" />    
                        </div>
                    </div>
                    <div class="col-sm">
                        <label for="skillob">Skills préférables</label> 
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom compétence" id="skillob" v-model="inp_pref">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="add_elem(skill_pref, inp_pref)">Ajout</button>
                            </div>
                        </div>

                        <ul class="list-group">
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillp, index) in skill_pref">
                               {{ skillp }}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_pref,index)">-</span>
                            </li>
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_pref">Nombre points</label>
                            <input id="percentage_pref" type="number" v-model="score_pref" />
                        </div>
                    </div>
                    <div class="col-sm">
                        <label for="skillob">Skills optionnelles</label> 
                        
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom compétence" id="skillob" v-model="inp_opt">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="add_elem(skill_opt, inp_opt)">Ajout</button>
                            </div>
                        </div>
                    
                        <ul class="list-group">
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillop,index) in skill_opt">
                              {{ skillop }}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_opt,index)">-</span>
                            </li>
        
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_opt">Nombre points</label>
                            <input id="percentage_opt" type="number" v-model="score_opt" />
                        </div>

                    </div>
                </div>
              </form>
        <button class="btn btn-outline-secondary mt-5" type="button" id="button-addon2" v-on:click="submit_form()">Enregistrer l'annonce</button>

    </div>
</template>
<style>

 .badge.badge-secondary{
    color: white;
   background-color: salmon;
 }
 .btn-outline-secondary, .btn-outline-secondary:active, .btn-outline-secondary:visited {
    background-color: white;
    color: salmon !important;
    border-color: salmon !important;
}
.btn-outline-secondary:hover{
    background-color: salmon !important;
    color: white !important;
    border-color: salmon !important;
}
</style>
<script>
import axios from 'axios'
export default {
    name : "NewAdvert",
    data(){
        return{
            nom_annonce : "",
            nom_employeur : "",
            inp_ob : "",
            inp_pref : "",
            inp_opt : "",
            score_ob : 50,
            score_pref : 40,
            score_opt : 10,
            skill_ob : [],
            skill_pref : [],
            skill_opt : []
        }
    },
    methods:{
        add_elem : function(table, elem){
            table.push(elem)
        },
        rem_elem : function(table, index){
            table.splice(index, 1)
        },
        submit_form : function(){
                axios.post('http://localhost:5001/annonce', {

                    name : this.nom_annonce,
                    employer : this.nom_employeur ,
                    obl : this.score_ob,
                    opt : this.score_opt,
                    pref : this.score_pref,
                    skill_ob : this.skill_ob,
                    skill_pref : this.skill_pref,
                    skill_opt : this.skill_opt
                }).then(() => {
                    alert("ok")
                })
                .catch((error) => {
                    console.log(error);
                });

            }

    }
}
</script>