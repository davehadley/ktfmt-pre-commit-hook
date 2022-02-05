# ktfmt-pre-commit-hook

[![Main Build status](https://img.shields.io/github/workflow/status/davehadley/ktfmt-pre-commit-hook/ci/main?label=main)](https://github.com/davehadley/ktfmt-pre-commit-hook)
[![Develop status](https://img.shields.io/github/workflow/status/davehadley/ktfmt-pre-commit-hook/ci/develop?label=develop)](https://github.com/davehadley/ktfmt-pre-commit-hook)
[![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)](https://github.com/davehadley/ktfmt-pre-commit-hook)
[![Last commit](https://img.shields.io/github/last-commit/davehadley/ktfmt-pre-commit-hook/develop)](https://github.com/davehadley/ktfmt-pre-commit-hook)
[![Last release](https://img.shields.io/github/release-date/davehadley/ktfmt-pre-commit-hook)](https://github.com/davehadley/ktfmt-pre-commit-hook)

A [pre-commit](https://pre-commit.com/) hook to run [ktfmt](https://github.com/facebookincubator/ktfmt).

## Requirements

This commit hook requires Python `>=3.8`.

`ktfmt` requires Java 11. The `java` in your `PATH` must be version `>=11`.

## Usage Instructions

Add the following lines to your `.pre-commit-config.yaml`.

```yaml
- repo: https://github.com/davehadley/ktfmt-pre-commit-hook
  rev: 0.4.0
  hooks:
  - id: ktfmt
    stages: [commit]
```

To specify a specific version of `ktfmt` pass `--version=XX.YY.ZZ` with the `args` option. 
All other `args` provided will be passed onto `ktfmt`. For example:

```yaml
- repo: https://github.com/davehadley/ktfmt-pre-commit-hook
  rev: 0.4.0
  hooks:
  - id: ktfmt
    args: [--version=0.31, --dropbox-style]
    stages: [commit]
```

See the [ktfmt documentation](https://facebookincubator.github.io/ktfmt/) for supported command line arguments.

Please report any bugs in the [issue tracker](https://github.com/davehadley/ktfmt-pre-commit-hook/issues).

## Development Instructions

### Environment Setup

Run `source setup.sh` to setup the development environment.
This may be slow the first time that this is run as the virtual environment is created
and dependencies are installed.

### Testing

Run:

```
poetry install
poetry run pytest tests
```

## License

Licensed under either of

 * Apache License, Version 2.0
   ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
 * MIT license
   ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.