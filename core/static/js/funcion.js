//implementar función utilizando FETCH que permita mostrar la información de las mascotas
function mostrar(){
    let url='http://localhost:3000/clientes';
    fetch(url)
    .then(response => response.json())
    .then(data => mostrar(data))
    .catch(error => console.log(error))

    const mostrar=(data)=>{
        console.log(data);
        let texto=""
        for(i=0; i<data.length; i++)
        {
            texto+=`<tr>
                 <td>${data[i].id}</td>
                 <td>${data[i].nombre}</td>
                 <td>${data[i].arreglo}</td>
                 <td><img src="${data[i].foto}"></td>
                 <td>${data[i].valoracion}</td>
                 </tr>`
        }//for
        document.getElementById('telefo').innerHTML=texto;
    }
}