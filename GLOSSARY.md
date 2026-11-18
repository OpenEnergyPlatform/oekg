<!--SPDX-License-Identifier: MIT-->

# Open Energy Knowledge Graphs

This repository holds two knowledge graphs, the OEKG and the MHPKG, together with their schemas and
the tooling around them. This glossary fixes the words used when talking about them.

## Knowledge graphs

**OEKG**:
The Open Energy Knowledge Graph, which holds scenario bundles (study, report, scenarios) behind the
Open Energy Platform's factsheets. Its schema is a set of SHACL shapes.
_Avoid_: factsheet graph

**MHPKG**:
The municipal heat planning knowledge graph. Its schema is a LinkML schema that references MHPO.
_Avoid_: heat graph, KWP graph

**Example dataset**:
The single, complete, fictional dataset kept per knowledge graph to show and test its schema.
_Avoid_: sample, fixture, test data

## Viewer

**Viewer**:
The interactive web page that draws a knowledge graph from its source graph.
_Avoid_: visualiser, graph browser, frontend

**Source graph**:
The file a view is drawn from: a LinkML schema, a SHACL shapes file or an example dataset in Turtle.
_Avoid_: input, data file

**Schema graph**:
The classes, properties, ranges, cardinalities and enums of one schema, taken as a graph regardless
of whether the schema is LinkML or SHACL.
_Avoid_: model graph, ER diagram

**Schema view**:
The viewer's primary view, which draws a schema graph so a reader sees how a knowledge graph is
built.
_Avoid_: model view, class diagram

**Instance view**:
The viewer's secondary view, which draws the nodes and relations of one example dataset.
_Avoid_: data view, plan diagram (unless it is an MHPKG heat plan)

**Preview**:
The viewer as built from a pull request's head, published for as long as the pull request is open.
_Avoid_: staging, branch build
