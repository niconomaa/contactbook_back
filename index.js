const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type Query {
    me(uid: String!): Person
  }

 type Mutation {
   addNewContactPerson(phoneNumber: String!): Person
   markMeAsInfected(uid: String!): Person
   addPerson(phoneNumber: String!): Person  
  }

  type Person {
    uid: String
    phoneNumber : String
    verified: Boolean
    infected: Boolean
    contactedPersons: [Person]
  }

`;

const server = new ApolloServer({
  typeDefs,
  mocks: true,
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`)
});


