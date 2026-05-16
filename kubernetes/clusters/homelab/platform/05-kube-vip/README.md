# kube-vip

`kube-vip` advertises the internal Kubernetes API VIP `192.168.1.184` on the
LAN. It runs only on control-plane nodes in `kube-system`.

This is cluster plumbing, not public exposure. Keep individual control-plane IPs
available for break-glass access.
