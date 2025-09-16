# Include Liquidsoap libraries
%include "/home/beasty197/.opam/4.14.0/share/liquidsoap-lang/libs/fades.liq"
%include "/home/beasty197/.opam/4.14.0/share/liquidsoap-lang/libs/ffmpeg.liq"

# Logging configuration
settings.log.stdout := true
settings.log.file := true
settings.log.file.path := get_env("LOG_PATH", "/logs/liquidsoap.log")
settings.log.level := 3

# Timing configuration
settings.clock.max_latency := 15.0

# Telnet server configuration for control
settings.server.telnet := true
settings.server.telnet.bind_addr := "127.0.0.1"
settings.server.telnet.port := 1234

# --- Playback queue logic (hidden for security) ---
# Queue creation (track_queue, special_queue, normal_queue)
# ... (queue creation logic hidden)
# Crossfade application
# ... (crossfade logic hidden)
# Queue combination via fallback
# ... (fallback logic hidden)
# Final source
final_source = mksafe(source)

# --- Metadata handling (hidden for security) ---
# Variables for storing metadata
current_artist = ref("Unknown Artist")
current_title = ref("Unknown Title")
current_filename = ref("Unknown File")
current_timestamp = ref("")

# Functions for logging and sending metadata
# ... (track and queue logging logic hidden)
# ... (metadata sending to API logic hidden)

# Apply track and metadata logging
print("Applying track and metadata logging...")
# ... (logging application hidden)

# Create source with metadata for Icecast
final_source_with_metadata = metadata.map(fun (_) -> [("artist", current_artist()), ("title", current_title()), ("comment", "File: " ^ current_filename())], final_source)

# --- Telnet commands (minimal set, rest hidden) ---
server.register("get_status", fun (_) -> "Status: OK")

# --- Other Telnet commands for queue management (hidden) ---
# ... (logic for adding tracks, skipping, getting queue contents hidden)

# Output stream to Icecast
print("Starting Icecast output...")
output.icecast(
    %mp3(bitrate=128),
    host = "localhost",
    port = 8000,
    password = get_env("ICECAST_PASSWORD", "default_password"),
    mount = "radio_stream",
    name = "VTRNK Internet Radio",
    description = "Internet radio station",
    final_source_with_metadata,
    on_connect = fun () -> print("Successfully connected to Icecast at /radio_stream"),
    on_disconnect = fun () -> print("Disconnected from Icecast at /radio_stream")
)

print("Liquidsoap setup complete!")