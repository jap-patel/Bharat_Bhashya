var crime_category={
    category : { 
        "Drug Crimes" : "Drug Crimes" , "Street Crime" : "Street Crime" , "Organized Crime" : "Organized Crime" ,
        "Political Crime" : "Political Crime" , "Victimless Crime" : "Victimless Crime" , "White Collar Crime" : "White Collar Crime" ,
    },

    subcategory : {
        "Drug Crimes" : [
            {"code" : "DD" , "name" : "Drug Dealing"},{"code" : "DT" ,"name" : "Drug Trafficking"},
            {"code" : "ML" , 'name' : "Manufacturing illegal drugs"},{"code" : "DP", "name" : "Drug Paraphernaila"},
            /*drug paraphernaila means sometype of equipment which is used to inject,prepare or inhale illegal drugs like pipes,bones,syrings,injections etc.*/
        ],

        "Street Crime" : [
            {"code" : "MR" , "name" : "Murder"},{"code" : "BI" , "name" : "Bodly uinjuery"},{"code" : "RE" , "name" : "Rape"},{"code" : "TT" , "name" : "Theft"},
            {"code" : "RR" , "name" : "Robbery"},{"code" : "PP" , "name" : "Pickpocketing"},{"code" : "HM" , "name" : "Hooliganism"},{"code" : "VM" , "name" : "Vandalism"},
            {"code" : "IW" , "name" : "Illegal posession of weapon"},{"code" : "GT" , "name" : "Graffiti"},{"code" : "PT" , "name" : "Prostitution"},{"code" : "KD" , "name" : "Kidnapping"},
        ],
        
        "Organized Crime" : [
            {"code" : "DT" , "name" : "Drug Trafficking"},{"code" : "HT" , "name" : "Human Trafficking"},{"code" : "CC" , "name" : "Cyber Crime"},
            {"code" : "ML" , "name" : "Money Laundering"},{"code" : "EN" , "name" : "Extortion"},{"code" : "AR" , "name" : "Armed Robbery"},{"code" : "CF" , "name" : "Counter Feiting"},
        ],

        "Political Crime" : [
            {"code" : "BB" , "name" : "Bribery"},{"code" : "TS" , "name" : "Treason"},{"code" : "SN" , "name" : "Sedition"},
            {"code" : "EP" , "name" : "Espionage"},{"code" : "TF" , "name" : "Theft"},{"code" : "PJ" , "name" : "Perjury"},
        ],

        "Victimless Crime" : [
            {"code" : "PT" , "name" : "Prostitution"},{"code" : "AS" , "name" : "Assiste Suicide"},{"code" : "TR" , "name" : "Trespassing"},{"code" : "RU" , "name" : "Recreational drug use"},
            {"code" : "GB" , "name" : "Gambling"},{"code" : "HS" , "name" : "Homelessness"},{"code" : "PD" , "name" : "Public Drukeness"},{"code" : "PN" , "name" : "Public Nudity"},
            {"code" : "PC" , "name" : "Possession of contraband"},
        ],

        "White Collar Crime" : [
            {"code" : "FD" , "name" : "Fraud"},{"code" : "IT" , "name" : "Insider Trading"},{"code" : "PS" , "name" : "Ponzi Scheme"},{"code" : "EM" , "name" : "Embezzlement"},
            {"code" : "CF" , "name" : "Counterfeiting"},{"code" : "ML" , "name" : "Money Laundring"},{"code" : "EG" , "name" : "Espionage"},
        ]
    }
}