FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /src

# Copy full source so we can build the binary inside the container.
# This avoids relying on any host-built artifacts (e.g., macOS dist/ outputs).
COPY . .

# PyInstaller needs a compiler toolchain for some deps; keep it minimal.
RUN apk add --no-cache gcc musl-dev python3-dev

RUN uv pip install --system pyinstaller

RUN if [ -f quantlib.spec ]; then \
			pyinstaller --clean --noconfirm quantlib.spec; \
		else \
			pyinstaller --clean --noconfirm --onefile --name quantlib quantlib_launcher.py; \
		fi


FROM alpine:3.23

ARG VERSION
LABEL org.opencontainers.image.version=$VERSION

RUN apk add --no-cache ca-certificates

COPY --from=builder /src/dist/quantlib /usr/local/bin/quantlib

ENTRYPOINT ["/usr/local/bin/quantlib"]
