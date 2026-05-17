FROM busybox:1.37.0-musl AS rootfs

RUN mkdir -p /out/rootfs/usr/local/bin /out/rootfs/usr/bin \
    && cp /bin/busybox /out/rootfs/usr/local/bin/busybox \
    && ln -s ../local/bin/busybox /out/rootfs/usr/bin/mountpoint

FROM scratch
COPY manifest.yaml /
COPY --from=rootfs /out/rootfs /rootfs
