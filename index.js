const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type Query {
    me: Person
  }

  type Person {
    id: String
    phoneNumber: String
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
