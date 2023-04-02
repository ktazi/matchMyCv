<template>
<div class="container">
    <h1 class="display-3 mt-5 mb-5">Score de l'annonce : {{ annonce.nom }}</h1>
    <button class="btn btn-outline-secondary" type="button" id="button-addon2" v-on:click="score()">Estimer les scores</button>
    <table class="table table-striped mt-5">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col"> <h4>Titre CV</h4></th>
                    <th scope="col"><h4>Score</h4></th>
                    <th scope="col"><h4>Visité</h4></th>
                    <th scope="col"><h4>Noter</h4></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="cv in cvs" v-if="!cv.visited"  >
                        <th scope="row">{{ cv.id }}</th>
                        <td>{{ cv.nom }}</td>
                        <td>{{ cv.predicted_score }} (estimation)</td>
                        <td v-if="cv.visited">VRAI</td>
                        <td v-else>FAUX</td>
                        <td v-if="cv.parsed"><router-link class="btn btn-outline-secondary" :to="'/note/'+annonce.id.toString()+'/'+ cv.id">Noter</router-link></td>
                        <td v-else><p>Attendre la conversion ...</p></td>                    
                </tr>
                <tr v-else style="background-color:#72ecfa;" >
                        <th scope="row">{{ cv.id }}</th>
                        <td>{{ cv.nom }}</td>
                        <td>{{ cv.score }}</td>
                        <td v-if="cv.visited">VRAI</td>
                        <td v-else>FAUX</td>
                        <td v-if="cv.parsed"><router-link class="btn btn-outline-secondary" :to="'/note/'+annonce.id.toString()+'/'+ cv.id">Noter</router-link></td>
                        <td v-else><p>Attendre la conversion ...</p></td>                    
                </tr>
                
            </tbody>
</table>
</div>
</template>
<script>

import axios from 'axios'

export default {
    name : "ScoreAffichage",
    data(){
        return {
            annonce : {id : 0, nom : "test"},
            cvs : [
                {nom : "cv", id : 1, score : 10, parsed: false},
                {nom : "cv2", id : 2, score : 30, parsed: false},
                {nom : "cv3", id : 3, score : 40, parsed: false},
                {nom : "cv4", id : 4, score : null, parsed: false},
                {nom : "cv5", id : 5, score : null,  parsed: false}
            ]
        }
    }, 
    mounted(){
        this.annonce.id = this.$route.params.id
        axios.get('http://localhost:5001/info', { params: {id_annonce: this.annonce.id} }).then(response => {
            this.annonce.nom = response.data.annonce[0][1]
            axios.get('http://localhost:5001/cv', { params: {id_annonce: this.annonce.id} }).then(resp =>{
                console.log(resp.data)
                this.cvs = []
                for (let i =0; i < resp.data.length; i++){
                    this.cvs.push({
                        nom : resp.data[i][2], 
                        score : resp.data[i][4],
                        id : resp.data[i][0],
                        parsed : resp.data[i][1],
                        predicted_score : resp.data[i][5],
                        visited : resp.data[i][6]
                    })
                }
                
            })
        })
    },
    methods :{
        score : function(){
            axios.post('http://localhost:5001/estimNoteAnnonce', {id_annonce:this.annonce.id})
        }   
    }
}
</script>