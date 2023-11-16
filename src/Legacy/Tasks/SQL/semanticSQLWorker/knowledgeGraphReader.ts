export const knowledgeGraph = {
    Profession: {
        label: "profession",
        alias: [{ sing: "profession", plur: "professions" }],
    },
    Person: {
        label: "person",
        alias: [
            {
                sing: "person",
                plur: "persons",
            },
        ],
        edges: [
            {
                id: "Title",
                label: "workAs",
                type: "relation",
                target: "Title",
                properties: {
                    job: {},
                },
            },
            {
                id: "personId",
                label: "ID",
                type: "attribute",
                target: "",
                properties: {},
            },
        ],
    },
};

interface IAlias {
    sing: string;
    plur: string;
}

export interface IStructuredKnowledgeGraph {
    [key: string]: {
        [key: string]: {
            alias: Array<IAlias>;
            unit?: string;
        };
    };
    // minorEntities: {
    //     [key: string]: {
    //         alias: Array<IAlias>;
    //         unit?: string;
    //     };
    // };
    // majorAttributes: {
    //     [key: string]: {
    //         alias: Array<IAlias>;
    //         unit?: string;
    //     };
    // };
    // minorAttributes: {
    //     [key: string]: {
    //         alias: Array<IAlias>;
    //         unit?: string;
    //     };
    // };
    // semanticEdges: {
    //     [key: string]: {
    //         alias: Array<IAlias>;
    //         unit?: string;
    //     };
    // };
}

const nodes = {
    person: {
        alias: [{ sing: "person", plur: "persons" }],
    },
    title: {
        alias: [{ sing: "title", plur: "titles" }],
    },
    profession: {
        alias: [{ sing: "profession", plur: "professions" }],
    },
    genre: {
        alias: [{ sing: "genre", plur: "genres" }],
    },
    name: {
        alias: [{ sing: "name", plur: "names" }],
    },
    year: {
        alias: [{ sing: "year", plur: "years" }],
    },
    format: {
        alias: [{ sing: "format", plur: "formats" }],
    },
    localization: {
        alias: [{ sing: "localization", plur: "localizations" }],
    },
    region: {
        alias: [{ sing: "region", plur: "regions" }],
    },
    language: {
        alias: [{ sing: "language", plur: "languages" }],
    },
    title_name: {
        alias: [{ sing: "name of title", plur: "name of titles" }],
    },
};

// majorEntities: Relations that only possess hasA- and semantic edges
// minorEntities: Relations that possess belongsTo-edges with cardinality n-m
// majorAttributes: Relations that possess belongsTo-edges with cardinality 1-m
// minorAttributes: Columns (naturally cardinality 1-1)
// semanticEdges: Junction-Relations with hasA-edges (naturally connecting tables with cardinality n-m)
export const structuredKnowledgeGraph: IStructuredKnowledgeGraph = {
    majorEntities: {
        person: {
            alias: [{ sing: "person", plur: "persons" }],
        },
        title: {
            alias: [{ sing: "title", plur: "titles" }],
        },
    },
    minorEntities: {
        profession: {
            alias: [{ sing: "profession", plur: "professions" }],
        },
        genre: {
            alias: [{ sing: "genre", plur: "genres" }],
        },
        language: {
            alias: [{ sing: "language", plur: "languages" }],
        },
        format: {
            alias: [{ sing: "format", plur: "formats" }],
        },
        name: {
            alias: [{ sing: "name", plur: "names" }],
        },
        year: {
            alias: [{ sing: "year", plur: "years" }],
        },
    },
    majorAttributes: {
        localization: {
            alias: [{ sing: "localization", plur: "localizations" }],
        },
    },
    minorAttributes: {
        year: {
            alias: [{ sing: "year", plur: "years" }],
        },
        year_id: {
            alias: [{ sing: "year identifier", plur: "year identifiers" }],
        },
        genre: {
            alias: [{ sing: "title genre", plur: "title genres" }],
        },
        genre_id: {
            alias: [{ sing: "genre identifier", plur: "genre identifiers" }],
        },
        person_id: {
            alias: [{ sing: "person identifier", plur: "person identifiers" }],
        },
        name: {
            alias: [{ sing: "name", plur: "names" }],
        },
        name_id: {
            alias: [{ sing: "name identifier", plur: "name identifiers" }],
        },
        birth_year: {
            alias: [{ sing: "year of birth", plur: "year of birth" }],
        },
        birthyear_id: {
            alias: [{ sing: "birthyear identifier", plur: "birthyear identifiers" }],
        },
        death_year: {
            alias: [{ sing: "year of death", plur: "year of death" }],
        },
        deathhyear_id: {
            alias: [{ sing: "deathyear identifier", plur: "deathyear identifiers" }],
        },
        profession_id: {
            alias: [{ sing: "profession identifier", plur: "profession identifiers" }],
        },
        profession: {
            alias: [{ sing: "profession", plur: "professions" }],
        },
        title_id: {
            alias: [{ sing: "title identifier", plur: "title identifiers" }],
        },
        format: {
            alias: [{ sing: "format", plur: "formats" }],
        },
        format_id: {
            alias: [{ sing: "format identifier", plur: "format identifiers" }],
        },
        title_name: {
            alias: [{ sing: "name of title", plur: "name of titles" }],
        },
        title_name_id: {
            alias: [{ sing: "title-name identifier", plur: "title-name identifiers" }],
        },
        is_adult: {
            alias: [{ sing: "rated adult", plur: "rated adult" }],
        },
        release_date_id: {
            alias: [{ sing: "release year identifier", plur: "release year identifiers" }],
        },
        runtime_minutes: {
            alias: [{ sing: "runtime", plur: "runtime" }],
            unit: "minutes",
        },
        average_rating: {
            alias: [{ sing: "average rating", plur: "average ratings" }],
        },
        vote_amount: {
            alias: [{ sing: "number of votes", plur: "number of votes" }],
        },
        localization_id: {
            alias: [{ sing: "localization identifier", plur: "localization identifiers" }],
        },
        region: {
            alias: [{ sing: "region", plur: "regions" }],
        },
        region_id: {
            alias: [{ sing: "region identifier", plur: "region identifiers" }],
        },
        language: {
            alias: [{ sing: "language", plur: "languages" }],
        },
        language_id: {
            alias: [{ sing: "language identifier", plur: "language identifiers" }],
        },
    },
    semanticEdges: {
    },
};
