'use Client'
import { useState} from "react";
export default function Correlation({selectedCat,onChange}){
   const categories=["PRODUITS ALIMENTAIRES ET BOISSONS NON ALCOOLISEES","BOISSONS ALCOOLISEES, TABAC ET STUPEFIANTS","ARTICLES D'HABILLEMENT ET CHAUSSURES","LOGEMENT, EAU, GAZ, ELECTRICITE ET AUTRES COMBUSTIBLES","MEUBLES, ARTICLES DE MENAGE ET ENTRETIEN COURANT DU FOYER","SANTE","TRANSPORTS","COMMUNICATIONS","LOISIRS ET CULTURE","ENSEIGNEMENT","RESTAURANTS ET HOTELS","BIENS ET SERVICES DIVERS"]
   return(
      <div className="flex  flex-wrap gap-6 items-center">
          <label className="text-sm font-medium text-gray-600">catégorie:</label>
         <select 
         className="p-2 rounded border border-gray-300 w-40 text-sm  max-w-full truncate"
         value={selectedCat}
         onChange={onChange}
         >
           { categories.map((a)=>(
               <option key={a} value={a}>
                  {a.toLowerCase()}
                  </option>
            ))}
         </select>
      </div>
   )
}
