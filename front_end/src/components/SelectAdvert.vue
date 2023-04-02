<template>
    <div class="container">
        <h1 class="display-3 mb-5 mt-5"> Sélection d'annonce </h1>
        <table class="table table-striped ">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col"> <h4>Nom annonce</h4></th>
                    <th scope="col"><h4>Nom employeur</h4></th>
                    <th scope="col"><h4>Modifier</h4></th>
                    <th scope="col"><h4>Scores</h4></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="annonce in annonces">
                    <th scope="row">{{ annonce.id }}</th>
                    <td>{{ annonce.nom }}</td>
                    <td>{{ annonce.employeur }}</td>
                    <td><router-link class="btn btn-outline-secondary" :to="'/modifAnnonce/'+annonce.id.toString()">Modifier</router-link></td>
                    <td><router-link class="btn btn-outline-secondary" :to="'/score/'+annonce.id.toString()">Score</router-link></td>

                </tr>
            </tbody>
        </table>
        <router-link class="btn btn-outline-secondary mt-5" to="/new">Ajouter une annonce</router-link>
    </div>
</template>
<script>
import axios from 'axios'

export default {
    name : "SelectAdvert",
    data(){
        return {
            annonces : [
                {nom : "Nom ", id : 1, employeur : "employeur"},
                {nom : "Nom 2", id : 2, employeur : "employeur 2"},
                {nom : "Nom 3", id : 3, employeur : "employeur 3"},
                {nom : "Nom 4", id : 4, employeur : "employeur 4"},
                {nom : "Nom 5", id : 5, employeur : "employeur 5"}
            ]
        }
    }, 
    mounted(){
        axios.get('http://localhost:5001/annonce')
    .then(response => {
        console.log(response.data)
        this.annonces = []
        for (let i =0; i < response.data.length; i++){
            this.annonces.push({nom:response.data[i][1], id:response.data[i][0], employeur:response.data[i][5]})
        }
    
    });
    }
}
</script>
<style>



 .table-striped>tbody>tr:hover{
    background-color: #fdddda !important;
    color:salmon !important;
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