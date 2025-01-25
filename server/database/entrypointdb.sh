#!/bin/bash
set -e

mongo <<EOF
use dealershipsDB
db.createUser({
    user: "username",
    pwd: "password",
    roles: [{ role: "readWrite", db: "yourDatabase" }]
});
EOF

# Execute the original entrypoint
exec "$@"
