def build_dependency_graph(packages):
    graph = {}

    for pkg in packages:
        name = pkg["name"]
        deps = pkg.get("dependencies", [])

        graph[name] = deps

    return graph


def remove_dev_dependencies(graph, dev_group):
    runtime_nodes = set()

    stack = list(dev_group)

    while stack:
        node = stack.pop()

        if node in runtime_nodes:
            continue

        runtime_nodes.add(node)

        for dep in graph.get(node, []):
            stack.append(dep)

    return runtime_nodes