The imports are indicated as "Pkg" and are in c2PtAbflPkg
```
commit;repo;time;Author;blob;file;language;package1;....
```

For example, find loranode

```
for i in {0..127}
do zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU0.s| grep -i loranode
done
```


The map from a commit to root and head commit is in c2rhpFullU{0..31}.gz
```
commit;root commit;distance to root;headcommit;head comit;distance to head;clique id (of connected commits)
```


