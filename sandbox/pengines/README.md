# Pengines Server Setup

This directory contains everything you need to run a local pengines server on your laptop.

## Prerequisites

- SWI-Prolog installed (✓ You have version 9.0.4)
- The pengines library (✓ Available in your SWI-Prolog installation)

## Quick Start

### Option 1: Simple Pengines Server (Recommended for beginners)

```bash
cd /home/calang/proyects/escuela/timetable/tt_db/sandbox/pengines
swipl -s simple_server.pl
```

This starts a pengines server on port 3030 with your genealogist application loaded.

### Option 2: Web-based Server (Advanced)

```bash
cd /home/calang/proyects/escuela/timetable/tt_db/sandbox/pengines
swipl -s web_pengine_server.pl
```

This starts a full HTTP server with a web interface at http://localhost:3030

### Option 3: Using the Startup Script

```bash
cd /home/calang/proyects/escuela/timetable/tt_db/sandbox/pengines
./start_server.sh simple    # or
./start_server.sh web
```

## Testing Your Server

### Method 1: Using the Test Client

In another terminal:
```bash
cd /home/calang/proyects/escuela/timetable/tt_db/sandbox/pengines
swipl -s test_client.pl -g main -t halt
```

### Method 2: Interactive Testing

```bash
swipl -s test_client.pl
?- test_genealogist_queries.
```

### Method 3: Manual Pengine Creation

```prolog
?- use_module(library(pengines)).
?- pengine_create([
    server('http://localhost:3030'),
    application(genealogist),
    ask(ancestor_descendant(mike, X))
], ID).
```

## Files in This Directory

- `simple_server.pl` - Basic pengines server (easiest to use)
- `web_pengine_server.pl` - Full HTTP server with web interface
- `pengine_server.pl` - Alternative simple server
- `test_client.pl` - Test client to verify server functionality
- `start_server.sh` - Convenience script to start servers
- `genealogist.pl` - Sample application with family relationships
- `load.pl` - Application loader configuration
- `peng_ex.pl` - Basic pengines example

## Available Queries (Genealogist Application)

Once your server is running, you can query:

- `ancestor_descendant(mike, X)` - Find descendants of mike
- `ancestor_descendant(X, sally)` - Find ancestors of sally
- `siblings(X, Y)` - Find all sibling pairs
- `parent_child(X, Y)` - Find all parent-child relationships
- `father_child(X, Y)` - Find father-child relationships
- `mother_child(X, Y)` - Find mother-child relationships

## Troubleshooting

### Server Won't Start
- Check if port 3030 is already in use: `netstat -tlnp | grep 3030`
- Try a different port by editing the server files

### Can't Connect from Client
- Make sure the server is running
- Check firewall settings
- Verify you're using the correct port (3030)

### Permission Issues
- Make sure start_server.sh is executable: `chmod +x start_server.sh`

## Security Notes

- The simple server allows connections from anywhere (`allow('*')`)
- For production use, restrict to localhost only by removing the `allow('*')` line
- Consider using authentication for public-facing servers

## Next Steps

1. **Add Your Own Applications**: Create new .pl files and register them with `pengine_application/1`
2. **Customize the Server**: Modify port, security settings, or add new features
3. **Build Web Interfaces**: Use the pengines JavaScript library to create web frontends
4. **Scale Up**: Consider using nginx or Apache as a reverse proxy for production

## Example Usage Session

```bash
# Terminal 1: Start server
$ swipl -s simple_server.pl

# Terminal 2: Test client
$ swipl -s test_client.pl -g main -t halt
Testing pengines server...

--- Find all ancestors of sally ---
  Result: ['X'=tom]
  Result: ['X'=trude]
  Result: ['X'=mike]

--- Find all descendants of mike ---
  Result: ['X'=tom]
  Result: ['X'=sally]
  Result: ['X'=ericka]

--- Find all siblings ---
  Result: ['X'=ericka, 'Y'=sally]

Test completed.
```

## API Reference

For advanced usage, see the SWI-Prolog pengines documentation:
- http://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/pengines.html%27)
