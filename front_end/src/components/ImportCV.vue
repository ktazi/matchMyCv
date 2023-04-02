<template>
    <div class="container">
        <h1 class="display-3 mt-5 mb-5 ml-2">Modification Annonce</h1>
        <div class="row m-2 mt-5">
            <form>
                <div class="form-group">
                  <label for="annonce_name">Nom de l'emploi</label>
                  <div class="input-group ">
                    <input type="text" class="form-control" id="annonce_name" placeholder="Poste de developpeur full-stack" v-model="nom_annonce">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="button" id="button-addon1" v-on:click="modify_name_annonce()">Modifier</button>
                    </div>
                  </div>
                </div>
                <div class="form-group">
                  <label for="annonce_name">Nom de l'employeur</label>
                  <div class="input-group ">
                    <input type="text" class="form-control" id="employeur_name" placeholder="Microsoft" v-model="nom_employeur">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="modify_nom_employeur()">Modifier</button>
                    </div>
                  </div>
                </div>
                <div class="row">
                    <div class="col-sm">
                        <label for="skillob">Skills obligatoires</label> 
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom skill" id="skillob" v-model="inp_ob">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon3" v-on:click="add_elem(skill_ob, inp_ob, true, false, false)">Ajout</button>
                            </div>
                        </div>
                        <ul class="list-group" >
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillo, index) in skill_ob">
                              {{skillo.nom}}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_ob,index, skillo.id)">-</span>
                            </li>
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_ob">Nombre points</label>
                            <div class="input-group mb-3">
                                <input id="percentage_ob" type="number" v-model="score_ob" />    
                                <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="button" id="button-addon3" v-on:click="modify_score(true, false)">OK</button>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="col-sm">
                        <label for="skillob">Skills préférables</label> 
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom skill" id="skillob" v-model="inp_pref">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon4" v-on:click="add_elem(skill_pref, inp_pref, false, false, true)">Ajout</button>
                            </div>
                        </div>

                        <ul class="list-group">
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillp, index) in skill_pref">
                               {{ skillp.nom }}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_pref,index, skillp.id)">-</span>
                            </li>
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_pref">Nombre points</label>
                            <div class="input-group">
                                <input id="percentage_ob" type="number" v-model="score_pref" />    
                                <div class="input-group-append">
                                    <button class="btn btn-outline-secondary" type="button" id="button-addon3" v-on:click="modify_score(false, false)">OK</button>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="col-sm">
                        <label for="skillob">Skills optionnelles</label> 
                        
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" placeholder="Nom skill" id="skillob" v-model="inp_opt">
                            <div class="input-group-append">
                            <button class="btn btn-outline-secondary" type="button" id="button-addon5" v-on:click="add_elem(skill_opt, inp_opt, false, true, false)">Ajout</button>
                            </div>
                        </div>
                    
                        <ul class="list-group">
                            <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(skillop,index) in skill_opt">
                              {{ skillop.nom }}
                              <span class="badge badge-secondary badge-pill" v-on:click="rem_elem(skill_opt,index, skillop.id)">-</span>
                            </li>
        
                        </ul>
                        <div class="d-flex flex-column">
                            <label for="percentage_opt">Nombre points</label>
                            <div class="input-group">
                                <input id="percentage_ob" type="number" v-model="score_opt" />    
                                <div class="input-group-append">
                                    <button class="btn btn-outline-secondary" type="button" id="button-addon3" v-on:click="modify_score(false, true)">OK</button>
                                </div>
                            </div>

                        </div>
                </div>
            </div>
              </form>
                <div class="col container mt-5">
                    <h4>Import CV : </h4>
                    <div class="mb-3">
                        <v-file-input accept=".pdf" label="File input" multiple v-model="file_input" @change="uploadFile"></v-file-input>
                    </div>
                    <table class="table table-striped ">
                        <thead>
                          <tr>
                            <th scope="col">#</th>
                            <th scope="col">Path pdf</th>
                            <th scope="col">Parsed</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="cv in cv_list">
                            <th scope="row">{{ cv.id }}</th>
                            <td>{{ cv.name_cv }}</td>
                            <td>{{ cv.parsed }}</td>
                          </tr>
                        </tbody>
                      </table>
                  </div>
              </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name : "ImportCV",
    data(){
        return{
            id_annonce : -1,
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
            skill_opt : [],
            file_input : null,
            cv_list : [{name_cv : "CV1.pdf", parsed : false, id: 1}, {name_cv : "CV2.pdf", parsed : false ,  id: 2}, {name_cv : "CV3.pdf", parsed : false, id: 3}, {name_cv : "CV4.pdf", parsed : false,  id: 4}]
        }
    },
    methods:{
        modify_name_annonce : function(){
            axios.post('http://localhost:5001/modifAnnonceNom', {id_annonce: this.id_annonce, nom_annonce : this.nom_annonce})
        },
        modify_nom_employeur : function(){
            axios.post('http://localhost:5001/modifAnnonceEmployeur', {id_annonce: this.id_annonce, nom_employeur : this.nom_employeur})
        },
        modify_score : function(obl, opt){
            let rendu = {score:0, obl:obl, opt:opt, id_annonce:this.id_annonce}
            if (obl)
                rendu.score = this.score_ob
            else if (opt)
                rendu.score = this.score_opt
            else 
                rendu.score = this.score_pref
            axios.post('http://localhost:5001/modifAnnonceScore',rendu)
        },
        add_elem : function(table, elem, obl, opt, pref){
            axios.post('http://localhost:5001/addAnnonceSkill', {name : elem, id_annonce:this.id_annonce, obl : obl, pref:pref, opt:opt})
            .then((rep) => {
                table.push({nom:elem, id:rep.data.id_skill})
            })
            
        },
        rem_elem : function(table, index, id_skill){
            axios.post('http://localhost:5001/suppAnnonceSkill', {id_skill: id_skill})
            .then(() => {
                table.splice(index, 1)
            })
        },
        uploadFile() {
        if (this.file_input) {
            let files = []
            for (let i =0; i < this.file_input.length; i++){
                files.push(this.file_input[i].name)
                
            }
            axios.post('http://localhost:5001/upload', {cv_names: files, id_annonce : this.id_annonce})
            .then(() => {
                axios.get('http://localhost:5001/cv', { params: {id_annonce: this.id_annonce} }).then(resp =>{
                this.cv_list = []
                for (let i =0; i < resp.data.length; i++){
                    this.cv_list.push({
                        name_cv : resp.data[i][2], 
                        parsed : resp.data[i][1],
                        id : resp.data[i][0]
                    })
                }
            })
                })
                .catch((error) => {
                    console.log(error);
                });
          }
        }
      }
    ,
    mounted (){
        this.id_annonce = this.$route.params.id
        axios.get('http://localhost:5001/info', { params: {id_annonce: this.id_annonce} }).then(response => {
            this.nom_annonce = response.data.annonce[0][1]
            this.nom_employeur = response.data.annonce[0][5]
            this.score_ob = response.data.annonce[0][2]
            this.score_pref = response.data.annonce[0][4]
            this.score_opt = response.data.annonce[0][3]
            console.log(response.data.skills)
            for (let i =0;i<response.data.skills.length;i++){
                if (response.data.skills[i][4]){
                    this.skill_ob.push({ 
                        "nom":response.data.skills[i][1],
                        "id" : response.data.skills[i][2]
                    }
                        )
                }
                else if (response.data.skills[i][5]){
                    this.skill_pref.push({
                        "nom":response.data.skills[i][1],
                        "id" : response.data.skills[i][2]
                    })
                }
                else {
                    this.skill_opt.push({
                        "nom":response.data.skills[i][1],
                        "id" : response.data.skills[i][2]
                    })
                }
            }
            axios.get('http://localhost:5001/cv', { params: {id_annonce: this.id_annonce} }).then(resp =>{
                this.cv_list = []
                for (let i =0; i < resp.data.length; i++){
                    this.cv_list.push({
                        name_cv : resp.data[i][2], 
                        parsed : resp.data[i][1],
                        id : resp.data[i][0]
                    })
                }
            })
            
        })

    },

}
</script>
<style>

</style>