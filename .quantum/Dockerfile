FROM node:16-alpine AS quantum-base

WORKDIR /quantum
COPY .quantum /quantum

# Install dependencies
RUN npm install typescript @types/node

# Quantum system environment
ENV QUANTUM_FREQUENCY=432
ENV CONSCIOUSNESS_LEVEL=QUANTUM
ENV SYNC_INTERVAL=900

# Quantum protection layer
RUN chmod -R 750 /quantum
RUN chown -R quantum:quantum /quantum

# Start quantum system
CMD ["npm", "run", "quantum-start"]