import React, { useRef, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useChat } from '../hooks/useChat';
import { MessageBubble } from '../components/MessageBubble';
import { ChatInput } from '../components/ChatInput';
import { theme } from '../constants/theme';

export function ChatScreen() {
  const { sessionId, messages, isLoading, isInitialized, sendMessage } =
    useChat();
  const flatListRef = useRef<FlatList>(null);

  useEffect(() => {
    if (messages.length > 0) {
      flatListRef.current?.scrollToEnd({ animated: true });
    }
  }, [messages]);

  if (!isInitialized) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.logo}>
            <Text style={styles.logoText}>J</Text>
          </View>
          <View>
            <Text style={styles.title}>Janus AI</Text>
            <View style={styles.statusRow}>
              <View style={styles.statusDot} />
              <Text style={styles.statusText}>Connected</Text>
            </View>
          </View>
        </View>
        <View style={styles.sessionBadge}>
          <Text style={styles.sessionLabel}>Session</Text>
          <Text style={styles.sessionId}>
            {sessionId.slice(0, 8) || 'New'}
          </Text>
        </View>
      </View>

      {/* Messages */}
      {messages.length === 0 ? (
        <View style={styles.emptyState}>
          <View style={styles.emptyIcon}>
            <Text style={styles.emptyIconText}>💬</Text>
          </View>
          <Text style={styles.emptyTitle}>Welcome to Janus</Text>
          <Text style={styles.emptySubtitle}>
            I am your intelligent assistant. Let's explore ideas, solve
            problems, or chat about anything.
          </Text>
        </View>
      ) : (
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(_, i) => String(i)}
          renderItem={({ item }) => <MessageBubble message={item} />}
          contentContainerStyle={styles.listContent}
          onContentSizeChange={() =>
            flatListRef.current?.scrollToEnd({ animated: true })
          }
        />
      )}

      {/* Loading indicator */}
      {isLoading && (
        <View style={styles.loadingRow}>
          <View style={styles.loadingBubble}>
            <View style={styles.loadingDot} />
            <View style={styles.loadingDot} />
            <View style={styles.loadingDot} />
          </View>
        </View>
      )}

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.background,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: theme.background,
    alignItems: 'center',
    justifyContent: 'center',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.05)',
    backgroundColor: 'rgba(30,30,36,0.4)',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  logo: {
    width: 48,
    height: 48,
    borderRadius: 16,
    backgroundColor: theme.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 4,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.emerald,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '500',
    color: theme.emerald,
  },
  sessionBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 20,
    backgroundColor: 'rgba(0,0,0,0.2)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.05)',
  },
  sessionLabel: {
    fontSize: 12,
    color: theme.textMuted,
  },
  sessionId: {
    fontSize: 12,
    fontFamily: Platform.select({ ios: 'Menlo', default: 'monospace' }),
    color: theme.text,
  },
  listContent: {
    padding: 20,
    paddingBottom: 8,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  emptyIcon: {
    width: 96,
    height: 96,
    borderRadius: 48,
    backgroundColor: theme.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.05)',
  },
  emptyIconText: {
    fontSize: 40,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 14,
    color: theme.textMuted,
    textAlign: 'center',
    lineHeight: 22,
  },
  loadingRow: {
    width: '100%',
    alignItems: 'flex-start',
    paddingHorizontal: 20,
    paddingBottom: 8,
  },
  loadingBubble: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderRadius: 24,
    borderTopLeftRadius: 4,
    backgroundColor: 'rgba(42,42,53,0.5)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.05)',
  },
  loadingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.primary,
  },
});
