import { credentials } from "./CONST";
const awsconfig = {
  Auth: {
    Cognito: {
      userPoolId: credentials.userPoolId,
      userPoolClientId: credentials.userPoolClientId,
      loginWith: {
        email: true,
      },
    },
    authenticationFlowType: "USER_PASSWORD_AUTH",
  },
};
export default awsconfig;
