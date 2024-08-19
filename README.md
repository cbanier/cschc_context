# CSCHC Context

## Overview

`cschc_context` is a tool designed to generate a SCHC compression context for the `cschc` library from a JSON context produced by `microschc`.

## Features

- Converts JSON context from `microschc` to a format compatible with `cschc`, i.e. a list of `uint8_t`.
- Ensures seamless integration between `microschc` and `cschc`.