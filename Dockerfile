FROM alpine:3.19.1


RUN apk add vim

ENTRYPOINT [ "ash", "-c", "vim file > /dev/null 2>&1 && cat file"  ]
# ENTRYPOINT [ "ash", "-c", "vim file"  ]
