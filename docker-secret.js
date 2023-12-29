const { exec } = require("child_process");

const secret = ""
const username = ""
const name = ""
const namespace = ""

const b64 = (string) => Buffer.from(string).toString('base64')

const dockerconfigjson = JSON.stringify({"auths": {"registry.gitlab.com": {"username": username,"password": secret,"auth": b64(`${username}:${secret}`)}}})

const command = `kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
type: kubernetes.io/dockerconfigjson
metadata:
  name: ${name}
  namespace: ${namespace}
data:
  .dockerconfigjson: ${b64(dockerconfigjson)}
EOF`

exec(command, (error, stdout, stderr) => {
    if (error) {
        console.log(error.message);
        return;
    }
    if (stderr) {
        console.log(stderr);
        return;
    }
    console.log(stdout);
});