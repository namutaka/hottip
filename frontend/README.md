# frontend

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn run serve
```

### Compiles and minifies for production
```
yarn run build
```

### Run your tests
```
yarn run test
```

### Lints and fixes files
```
yarn run lint
```

### Run your unit tests
```
yarn run test:unit
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## graphql typescript

```
# see https://docs.graphene-python.org/projects/django/en/latest/introspection/#usage
pipenv run ./manage.py graphql_schema --schema hottip.schema.schema --out schema.json

# see https://medium.com/open-graphql/automatically-generate-typescript-definitions-for-graphql-queries-with-apollo-codegen-e73eae72b561
cd frontend; yarn run apollo codegen:generate --localSchemaFile=../schema.json --target=typescript --includes=src/graphql/\*.ts --tagName=gql --addTypename types
```

