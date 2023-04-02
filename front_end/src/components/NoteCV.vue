<template>
    <div>
        <div class="container" style="height: 100%; width: 100%;">
            <h1 class="display-3 mt-5 mb-5">Noter CV</h1>
                <div class="row" >
                    <div class="col-8" style=" height: 800px ">
                        <VuetifyPdf :url="'http://localhost:8080/api/pdf/'+pdf_url" id="pdf"></VuetifyPdf>
                    </div>
                <div class="col-4" style=" height: 100%; ">
                    <h5>Skills obligatoires</h5>
                    <div class="list-group list-group-flush mb-3">
                        <li class="list-group-item" v-for="obli in skills.obligatoire">
                            <input type="checkbox" v-model="obli[1]" v-on:change="change_check_status(obli[2])" /><span v-on:click="change_reco(obli[0])">{{ obli[0] }}</span>
                            <span class="badge badge-success badge-pill" v-if="obli[3]">MATCH FOUND !</span>
                            <br />
                        </li>
                    </div>
                    <h5>Skills preferables</h5>
                    <div class="list-group list-group-flush mb-3">
                        <li class="list-group-item" v-for="pref in skills.preferable">
                            <input type="checkbox" v-model="pref[1]" v-on:change="change_check_status(pref[2])"/><span v-on:click="change_reco(pref[0])">{{ pref[0] }}</span> 
                            <span class="badge badge-success badge-pill" v-if="pref[3]">MATCH FOUND !</span>
                            <br />
                        </li>
                    </div>
                    <h5>Skills optionnelles</h5>
                    <div class="list-group list-group-flush">
                        <li class="list-group-item" v-for="opt in skills.optionnel">
                            <input type="checkbox" v-model="opt[1]" v-on:change="change_check_status(opt[2])"/><span  v-on:click="change_reco(opt[0])">{{ opt[0] }}</span>
                            <span class="badge badge-success badge-pill" v-if="opt[3]"> MATCH FOUND !</span>
                            <br />
                        </li>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
 .badge.badge-success{
    color: black;
   background-color: #72ecfa;
 }
</style>
<script>
    import axios from 'axios'
    import VuetifyPdf from "vuetify-pdfjs/src/App.vue";
        export default {
        name : "NoteCV",
        data(){
            return{
                id_annonce : 1 ,
                pdf_url : "test.pdf",
                skills : {
                    obligatoire : [],
                    preferable : [],
                    optionnel : []
                },
                skill_temporaire : {
                    obligatoire : [],
                    preferable : [],
                    optionnel : []
                },
                recommandation : ["recommandation 1", "recommandation 2", "recommandation 3"]
            }
        },
        methods:{
            change_check_status : function(id_skill){
                axios.post('http://localhost:5001/checkCV', {id_cv: this.id_cv, id_skill : id_skill})
            },
            change_reco : function(name_skill){
                this.recommandation = [name_skill + " recommandation 1", name_skill + " recommandation 2", name_skill + " recommandation 3"]
            }
        },
        components :{
            VuetifyPdf
        },
        mounted : function(){
            this.id_annonce = this.$route.params.idannonce
            this.id_cv = this.$route.params.numcv
            axios.get('http://localhost:5001/isnote',{ params: {id_cv: this.id_cv}} ).then(()=>{
                axios.get('http://localhost:5001/infoCV', { params: {id_cv: this.id_cv} }).then(response => {
                console.log("test : ")
                console.log(this.id_cv)
                console.log(response.data)

                this.skill_temporaire.obligatoire = []
                this.skill_temporaire.preferable = []
                this.skill_temporaire.optionnel = []
                for (let i =0;i<response.data.length;i++){
                    if (response.data[i][2]){
                        this.skill_temporaire.obligatoire.push([response.data[i][5],response.data[i][6], response.data[i][1], false])
                    }
                    else if (response.data[i][4]){
                        this.skill_temporaire.preferable.push([response.data[i][5], response.data[i][6], response.data[i][1], false])
                    }
                    else {
                        this.skill_temporaire.optionnel.push([response.data[i][5], response.data[i][6],response.data[i][1], false])
                    }
            }
            axios.get('http://localhost:5001/cvdata', { params: {id_cv: this.id_cv} }).then(resp=>{
                this.pdf_url = resp.data[0][2]
                axios.get('http://localhost:5001/getRecommandation', { params: {id_cv: this.id_cv, pdf_name:this.pdf_url} }).then(rp=>{
                    console.log(rp.data)
                    console.log(this.skill_temporaire)
                    for (let key=0;key< Object.keys(rp.data).length;key++){
                        for (let i =0; i<this.skill_temporaire.obligatoire.length;i++){
                            if (this.skill_temporaire.obligatoire[i][2]==Object.keys(rp.data)[key]){
                                this.skill_temporaire.obligatoire[i][3] = rp.data[Object.keys(rp.data)[key]]
                            }
                        }
                        for (let i =0; i<this.skill_temporaire.preferable.length;i++){
                            if (this.skill_temporaire.preferable[i][2]==Object.keys(rp.data)[key]){
                                this.skill_temporaire.preferable[i][3] = rp.data[Object.keys(rp.data)[key]]
                            }
                        }
                        for (let i =0; i<this.skill_temporaire.optionnel.length;i++){
                            if (this.skill_temporaire.optionnel[i][2]==Object.keys(rp.data)[key]){
                                this.skill_temporaire.optionnel[i][3] = rp.data[Object.keys(rp.data)[key]]
                            }
                        }
                    }
                    this.skills.obligatoire = this.skill_temporaire.obligatoire
                    this.skills.preferable = this.skill_temporaire.preferable
                    this.skills.optionnel = this.skill_temporaire.optionnel
                    console.log(this.skills)
                })
            })
            })

            })
            
        }
    }    
</script>