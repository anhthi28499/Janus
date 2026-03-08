import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { Message } from '@janus/shared';
import { theme } from '../constants/theme';

interface MessageBubbleProps {
  message: Message;
}

function formatTime(isoString: string): string {
  const d = new Date(isoString);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <View style={[styles.row, isUser ? styles.rowUser : styles.rowAssistant]}>
      <View
        style={[
          styles.bubble,
          isUser ? styles.bubbleUser : styles.bubbleAssistant,
        ]}
      >
        <Text
          style={[styles.content, isUser ? styles.contentUser : styles.contentAssistant]}
        >
          {message.content}
        </Text>
        <Text
          style={[
            styles.timestamp,
            isUser ? styles.timestampUser : styles.timestampAssistant,
          ]}
        >
          {formatTime(message.timestamp || new Date().toISOString())}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    width: '100%',
    marginBottom: 16,
  },
  rowUser: {
    alignItems: 'flex-end',
  },
  rowAssistant: {
    alignItems: 'flex-start',
  },
  bubble: {
    maxWidth: '85%',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderRadius: 24,
  },
  bubbleUser: {
    backgroundColor: theme.primary,
    borderTopRightRadius: 4,
  },
  bubbleAssistant: {
    backgroundColor: theme.surfaceLight,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.05)',
    borderTopLeftRadius: 4,
  },
  content: {
    fontSize: 15,
    lineHeight: 22,
  },
  contentUser: {
    color: '#fff',
  },
  contentAssistant: {
    color: theme.text,
  },
  timestamp: {
    marginTop: 8,
    fontSize: 11,
    fontWeight: '500',
  },
  timestampUser: {
    color: 'rgba(255,255,255,0.7)',
    textAlign: 'right',
  },
  timestampAssistant: {
    color: theme.textMuted,
  },
});
