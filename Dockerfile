FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /src

# Optionally skip installing the toolchain (useful if you have a prebuilt builder image)
ARG SKIP_TOOLCHAIN=false

# Install minimal compiler toolchain and PyInstaller *before* copying source so this layer
# can be cached across builds unless the Dockerfile changes.
RUN if [ "$SKIP_TOOLCHAIN" = "false" ]; then \
        apk add --no-cache gcc musl-dev python3-dev && \
        uv pip install --system pyinstaller; \
    else \
        echo "Skipping toolchain install (SKIP_TOOLCHAIN=$SKIP_TOOLCHAIN)"; \
    fi

# Copy full source (this comes after toolchain install so source changes don't bust the above cache).
COPY . .

# Ensure the package is installable so PyInstaller can discover imports from `src/`
RUN python -m pip install --upgrade pip && python -m pip install .

RUN if [ -f quantlib.spec ]; then \
        # When a .spec is provided, PyInstaller doesn't accept --paths; we installed the package above
        pyinstaller --clean --noconfirm quantlib.spec; \
    else \
        pyinstaller --clean --noconfirm --onefile --name quantlib --paths=src quantlib_launcher.py; \
    fi


FROM alpine:3.23

ARG VERSION
LABEL org.opencontainers.image.version=$VERSION

RUN apk add --no-cache ca-certificates

COPY --from=builder /src/dist/quantlib /usr/local/bin/quantlib

ENTRYPOINT ["/usr/local/bin/quantlib"]
