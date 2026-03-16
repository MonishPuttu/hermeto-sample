def build_dependency_graph(packages):
    graph = {}

    for pkg in packages:
        name = pkg["name"]
        deps = pkg.get("dependencies", [])

        normalized = []

        for dep in deps:
            if isinstance(dep, dict):
                normalized.append(dep.get("name"))
            else:
                normalized.append(dep)

        graph[name] = normalized

    return graph


def remove_dev_dependencies(graph, dev_group):
    runtime_nodes = set()

    if not graph:
        return runtime_nodes

    roots = set(graph.keys()) - set(dev_group)

    stack = list(roots)

    while stack:
        node = stack.pop()

        if node in runtime_nodes:
            continue

        runtime_nodes.add(node)

        for dep in graph.get(node, []):
            if dep not in runtime_nodes:
                stack.append(dep)

    return runtime_nodes